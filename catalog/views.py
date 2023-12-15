import datetime
import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from localflavor.us.us_states import STATE_CHOICES
from photologue.models import Gallery
from photologue.views import GalleryListView, PhotoDetailView

import bookings.models
from bookings.forms import BillingInformationForm, ShippingInformationForm, PaymentForm
from bookings.models import Booking, Order, ShoppingCart
from .forms import OrderForm

logger = logging.getLogger(__name__)


def booking_confirmation(request):
    if not hasattr(request.user, 'client'):
        # If the user has no client profile, redirect them to a profile completion page
        return redirect('register_user')

    # Initialize forms outside of POST request handling
    billing_form = BillingInformationForm()
    shipping_form = ShippingInformationForm()
    payment_form = PaymentForm()

    if request.method == 'POST':
        billing_form = BillingInformationForm(request.POST)
        shipping_form = ShippingInformationForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if all([billing_form.is_valid(), shipping_form.is_valid(), payment_form.is_valid()]):
            # Process the valid forms
            billing = billing_form.save(commit=False)
            billing.client = request.user.client
            billing.save()

            shipping = shipping_form.save(commit=False)
            shipping.client = request.user.client
            shipping.save()

            payment = payment_form.save(commit=False)
            payment.client = request.user.client
            payment.billing_info = billing
            payment.save()

            # Handle booking IDs and create orders as necessary
            booking_ids = request.POST.getlist('booking_ids')
            bookings = Booking.objects.filter(booking_id__in=booking_ids)

            if not bookings.exists():
                messages.error(request, "Booking not found.")
                return HttpResponse('An error occurred: Booking not found.')

            cart, created = ShoppingCart.objects.get_or_create(client=request.user.client, confirmed=False)
            cart.bookings.set(bookings)
            cart.billing_information = billing
            cart.shipping_information = shipping
            cart.payment_information = payment
            cart.confirmed = True
            cart.save()

            for booking in bookings:
                order = Order(client=request.user, booking=booking)
                order.save()

            clear_cart(request)

            messages.success(request, "Your bookings have been confirmed!")
            return redirect('confirmation')

        else:
            # Gather the errors from the forms and render the page with these forms
            errors = billing_form.errors.as_data()
            errors.update(shipping_form.errors.as_data())
            errors.update(payment_form.errors.as_data())
            messages.error(request, "There was an error with your form submission. Please check your information.")

    # Render the booking confirmation page with the forms (empty for GET or with errors for POST)
    return render(request, 'booking_confirmation.html', {
        'billing_form': billing_form,
        'shipping_form': shipping_form,
        'payment_form': payment_form,
        'errors': errors if request.method == 'POST' else {},
    })


class CustomGalleryListView(GalleryListView):
    template_name = 'photologue/gallery_list.html'

    def get_queryset(self):
        return Gallery.objects.filter(title__icontains='')


class CustomPhotoDetailView(PhotoDetailView):
    template_name = 'photologue/photo_detail.html'


def index(request):
    context = {

    }

    return render(request, 'index.html', context=context)


def clear_cart(request):
    # Clear the cart session
    request.session['cart'] = []
    request.session.modified = True


def about(request):
    return render(request, 'about.html')


def senior_about(request):
    return render(request, 'senior_about.html')


def family_about(request):
    return render(request, 'family_about.html')


def couples_engagements_about(request):
    return render(request, 'couples_engagements_about.html')


def calendar(request):
    return render(request, 'calendar.html')


class CalendarView(generic.DetailView):
    model = Booking


def view_cart(request):
    # Initialize the cart if it doesn't exist
    if 'cart' not in request.session:
        request.session['cart'] = []

    # Retrieve booking_id from GET request and add to cart
    booking_id = request.GET.get('booking_id')
    if booking_id:
        try:
            booking_id = int(booking_id)  # Convert to integer
            # Add to cart if not already present
            if booking_id not in request.session['cart']:
                request.session['cart'].append(booking_id)
                request.session.modified = True  # Make sure to save the session
        except (TypeError, ValueError, Booking.DoesNotExist):
            logger.error("Invalid booking ID or booking not found")

    # Retrieve all bookings from the cart
    cart_booking_ids = request.session['cart']
    bookings = Booking.objects.filter(pk__in=cart_booking_ids)

    subtotal = sum(booking.package.price for booking in bookings if booking.package)
    tax = subtotal * 0.055
    total = subtotal + tax

    # TODO: Incorporate confirmation no. logic in next Sprint
    # confirmation = randint(50000, 100000)

    context = {
        'STATE_CHOICES': STATE_CHOICES,
        'bookings': bookings,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        # 'confirmation': confirmation,
    }

    return render(request, 'shopping_cart.html', context)


def calendar_view(request):
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)

    if month and year:
        currentDate = datetime.date(int(year), int(month), 1)
    else:
        currentDate = datetime.date.today()

    bookings_for_month = Booking.objects.filter(date__month=currentDate.month, date__year=currentDate.year)

    booked_dates = [b.date.day for b in bookings_for_month]

    return render(request, 'calendar.html', {'booked_dates': booked_dates, 'current_month': currentDate.month,
                                             'current_year': currentDate.year})


def order_history(request):
    if request.user.is_authenticated:
        # Get the orders associated with the logged-in user
        orders = Order.objects.filter(client=request.user).order_by('-created_at')
        return render(request, 'order_history.html', {'orders': orders})
    else:
        # Redirect to login page or handle accordingly
        pass


def order_information_input(request):
    # Retrieve booking_id from GET request
    booking_id = request.GET.get('booking_id')

    print(bookings)
    # If a booking ID is not provided, redirect back to the booking list
    booking = None

    if booking_id:
        try:
            booking = Booking.objects.get(pk=booking_id)
            logger.debug(f"Booking retrieved: {booking}")
        except Booking.DoesNotExist:
            logger.error(f"Booking with ID {booking_id} not found")

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Combine all context variables into one dictionary including the booking and STATE_CHOICES
            context = {
                'STATE_CHOICES': STATE_CHOICES,
                'booking': booking,
            }
            return render(request, 'order_information_input.html', context)
    else:
        # For a GET request, render the initial form and include the booking and STATE_CHOICES
        context = {
            'STATE_CHOICES': STATE_CHOICES,
            'booking': booking,
        }
        return render(request, 'order_information_input.html', context)


def remove_from_cart(request, booking_id):
    # Get the cart from the session and remove the booking_id
    cart = request.session.get('cart', [])

    if booking_id in cart:
        cart.remove(booking_id)
        request.session.modified = True  # Indicate that the session has been modified

    # Redirect back to the cart page
    return redirect('view_cart')

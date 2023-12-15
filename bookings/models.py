from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from localflavor.us.us_states import STATE_CHOICES
from datetime import date


class Package(models.Model):
    name = models.CharField('Package Name', max_length=120)
    description = models.CharField('Package Description', max_length=512)
    price = models.FloatField(blank=True)
    duration = models.CharField('Package Duration', max_length=15)
    owner = models.IntegerField("Photographer", blank=False, default=1)

    class Meta:
        db_table = 'package'
        verbose_name = "My  Package"
        verbose_name_plural = "My Packages"

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    class Meta:
        db_table = 'client'
        verbose_name = "My Client"
        verbose_name_plural = "My Clients"

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    name = models.CharField('Booking Name', max_length=120)
    date = models.DateTimeField('Booking Date')
    package = models.ForeignKey(Package, blank=True, null=True, on_delete=models.CASCADE)
    photographer = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    approved = models.BooleanField('Approved', default=False)

    class Meta:
        db_table = 'booking'
        verbose_name = "My Booking"
        verbose_name_plural = "My Bookings"

    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.date.date() - today
        days_till_stripped = str(days_till).split(",", 1)[0]
        return days_till_stripped

    @property
    def Is_Past(self):
        today = date.today()
        if self.date.date() < today:
            thing = "Past"
        else:
            thing = "Future"
        return thing


class BillingInformation(models.Model):
    billing_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    billing_address = models.CharField(max_length=512)
    billing_address2 = models.CharField(max_length=512, blank=True, null=True)
    billing_city = models.CharField(max_length=512)
    billing_state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    billing_zip = models.CharField(max_length=5, null=True, blank=True)
    billing_country = models.CharField(max_length=512, null=True, blank=True)
    phone_number = models.CharField(max_length=15)


class ShippingInformation(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=512)
    shipping_address2 = models.CharField(max_length=512, blank=True, null=True)
    shipping_city = models.CharField(max_length=512)
    shipping_state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    shipping_zip = models.CharField(max_length=5, null=True, blank=True)
    shipping_country = models.CharField(max_length=512, null=True, blank=True)
    phone_number = models.CharField(max_length=15)


class PaymentInformation(models.Model):
    payment_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    billing_info = models.ForeignKey(BillingInformation, on_delete=models.CASCADE)
    cc_number = models.IntegerField()
    cc_exp = models.CharField(max_length=5, blank=True, null=True)
    cvv_number = models.IntegerField()


class ShoppingCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bookings = models.ManyToManyField('Booking', related_name='shopping_carts')
    billing_information = models.ForeignKey(BillingInformation, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_information = models.ForeignKey(ShippingInformation, on_delete=models.SET_NULL, null=True, blank=True)
    payment_information = models.ForeignKey(PaymentInformation, on_delete=models.SET_NULL, null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.client.user.username}"


class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
                              default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(max_length=256, unique=True)
    date_subscribed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

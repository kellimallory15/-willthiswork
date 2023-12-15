from django import forms
from django.forms import ModelForm
from localflavor.us.forms import USStateField
from localflavor.us.models import USZipCodeField
from localflavor.us.us_states import STATE_CHOICES

from .models import Package, Booking, BillingInformation, ShippingInformation, PaymentInformation


# Admin SuperUser Event Form
class BookingFormAdmin(ModelForm):
    class Meta:
        model = Booking
        fields = ('name', 'date', 'package', 'photographer', 'notes', 'description')
        labels = {
            'name': '',
            'date': 'YYYY-MM-DD HH:MM:SS',
            'package': 'Photo Package',
            'photographer': 'Photographer',
            'description': 'Booking Description',
            'notes': 'Additional Notes',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Booking Name'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Booking Date'}),
            'package': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'photographer': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Notes'}),
        }


# User Event Form
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ('name', 'date', 'package', 'photographer', 'description')
        labels = {
            'name': '',
            'date': 'YYYY-MM-DD HH:MM:SS',
            'package': 'Photo Package',
            'description': 'Booking Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Booking Name'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Booking Date'}),
            'package': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'photographer': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


# Create a package form
class PackageForm(ModelForm):
    class Meta:
        model = Package
        fields = ('name', 'description', 'price', 'duration')
        labels = {
            'name': '',
            'description': '',
            'price': '',
            'duration': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Package Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Package Description'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '$0.00'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duration'}),
        }


class BillingInformationForm(forms.ModelForm):
    class Meta:
        model = BillingInformation
        fields = ['billing_address', 'billing_address2', 'billing_city', 'billing_state', 'billing_zip',
                  'billing_country', 'phone_number']

    billing_state = USStateField(widget=forms.Select(choices=STATE_CHOICES))
    billing_zip = USZipCodeField()


class ShippingInformationForm(forms.ModelForm):
    class Meta:
        model = ShippingInformation
        fields = ['shipping_address', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zip',
                  'shipping_country']

    shipping_state = USStateField(widget=forms.Select(choices=STATE_CHOICES))
    shipping_zip = USZipCodeField()


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentInformation
        fields = ['cc_number', 'cc_exp', 'cvv_number']

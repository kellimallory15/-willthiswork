from django.contrib import admin
from .models import Package, NewsletterSubscriber, BillingInformation, PaymentInformation, Order
from .models import Client
from .models import Booking
from django.contrib.auth.models import Group
from django.contrib import admin
from .models import ShippingInformation

admin.site.register(Client)

admin.site.unregister(Group)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    ordering = ('name',)
    search_fields = ('name', 'description')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    fields = (('name', 'package'), 'date', 'description', 'photographer', 'approved')
    list_display = ('name', 'date', 'package')
    list_filter = ('date', 'package')
    ordering = ('date',)


class ShippingInformationAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip', 'shipping_country',
        'phone_number')
    search_fields = ('client', 'shipping_address')
    list_filter = ('shipping_state', 'shipping_country')


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'booking', 'created_at', 'updated_at', 'status')
    search_fields = ('client', 'booking')
    list_filter = ('created_at', 'status')


class BillingInformationAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'billing_address', 'billing_city', 'billing_state', 'billing_zip', 'billing_country')
    search_fields = ('client', 'billing_address')
    list_filter = ('billing_state', 'billing_country')


class PaymentInformationAdmin(admin.ModelAdmin):
    list_display = ('cc_number', 'cc_exp', 'cvv_number')

    list_filter = ('cc_number', 'cc_exp', 'cvv_number')


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'date_subscribed')


admin.site.register(Order, OrderAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
admin.site.register(ShippingInformation, ShippingInformationAdmin)
admin.site.register(BillingInformation, BillingInformationAdmin)
admin.site.register(PaymentInformation, PaymentInformationAdmin)

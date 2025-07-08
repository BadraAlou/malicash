from django.contrib import admin
from .models import (
    Country, Currency, ExchangeRate, PaymentMethod, 
    TransferFee, Transfer, Agent
)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'symbol')
    search_fields = ('name', 'code')

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('from_currency', 'to_currency', 'rate', 'last_updated')
    list_filter = ('from_currency', 'to_currency')
    search_fields = ('from_currency__code', 'to_currency__code')
    date_hierarchy = 'last_updated'

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(TransferFee)
class TransferFeeAdmin(admin.ModelAdmin):
    list_display = ('from_country', 'to_country', 'payment_method', 'min_amount', 'max_amount', 'fee_fixed', 'fee_percentage')
    list_filter = ('from_country', 'to_country', 'payment_method')
    search_fields = ('from_country__name', 'to_country__name')

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('reference', 'sender', 'receiver_name', 'amount', 'fee', 'from_country', 'to_country', 'status', 'created_at')
    list_filter = ('status', 'from_country', 'to_country', 'payment_method', 'created_at')
    search_fields = ('reference', 'sender__username', 'receiver_name', 'receiver_phone')
    date_hierarchy = 'created_at'
    readonly_fields = ('reference', 'created_at', 'updated_at')

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'phone', 'is_active')
    list_filter = ('country', 'city', 'is_active')
    search_fields = ('name', 'address', 'city', 'phone')
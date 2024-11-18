from django.contrib import admin
from django.urls import path
from django.utils.html import format_html

from .admin_views import currency_converter_view
from .models import Currency, CurrencyExchangeRate

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "symbol")
    change_list_template = "admin/currency_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("currency-converter/", self.admin_site.admin_view(currency_converter_view), name="currency_converter_view"),
        ]
        return custom_urls + urls

    def currency_converter_link(self):
        return format_html('<a href="{}">Currency Converter</a>', "/admin/currency-converter/")

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyExchangeRate)

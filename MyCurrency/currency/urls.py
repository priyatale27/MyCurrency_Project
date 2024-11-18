from django.urls import path
from .views import CurrencyRatesList, CurrencyConverter
from .admin_views import currency_converter_view

urlpatterns = [
    path('rates/', CurrencyRatesList.as_view(), name='currency_rates'),
    path('convert/', CurrencyConverter.as_view(), name='currency_converter'),
    path('admin/currency-converter/', currency_converter_view, name='currency_converter_view'),

]

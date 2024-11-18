from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .models import CurrencyExchangeRate, Currency
from datetime import datetime

@staff_member_required
def currency_converter_view(request):
    converted_amount = None
    source_currency_code = request.GET.get("source_currency")
    target_currency_code = request.GET.get("target_currency")
    amount = request.GET.get("amount")

    if request.method == "GET" and source_currency_code and target_currency_code and amount:
        try:
            amount = float(amount)
            rate = CurrencyExchangeRate.objects.filter(
                source_currency__code=source_currency_code,
                exchanged_currency__code=target_currency_code,
                valuation_date=datetime.today()
            ).order_by("-valuation_date").first()

            if rate:
                converted_amount = amount * rate.rate_value
            else:
                converted_amount = "No exchange rate available for this currency pair on the selected date."

        except ValueError:
            converted_amount = "Invalid amount."

    currencies = Currency.objects.all()
    context = {
        "currencies": currencies,
        "converted_amount": converted_amount,
    }
    return render(request, "admin/currency_converter.html", context)

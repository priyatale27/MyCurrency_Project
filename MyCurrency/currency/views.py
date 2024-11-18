from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Currency, CurrencyExchangeRate
from .serializers import CurrencySerializer, CurrencyExchangeRateSerializer
from .services import get_exchange_rate_data

class CurrencyRatesList(APIView):
    def get(self, request):
        source_currency = request.query_params.get('source_currency')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        rates = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            valuation_date__range=[date_from, date_to]
        )
        serializer = CurrencyExchangeRateSerializer(rates, many=True)
        return Response(serializer.data)

class CurrencyConverter(APIView):
    def get(self, request):
        source_currency = request.query_params.get('source_currency')
        exchanged_currency = request.query_params.get('exchanged_currency')
        amount = float(request.query_params.get('amount'))
        rate = get_exchange_rate_data(source_currency, exchanged_currency, None, 'mock')
        converted_amount = amount * rate if rate else None
        return Response({"rate": rate, "converted_amount": converted_amount})




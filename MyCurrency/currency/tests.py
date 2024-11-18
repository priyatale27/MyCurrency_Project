from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from currency.models import Currency, CurrencyExchangeRate
from currency.services import get_exchange_rate_data
from datetime import datetime
from unittest.mock import patch

class CurrencyModelTestCase(TestCase):
    def setUp(self):
        self.currency = Currency.objects.create(code="USD", name="US Dollar", symbol="$")

    def test_currency_creation(self):
        self.assertEqual(self.currency.code, "USD")
        self.assertEqual(self.currency.name, "US Dollar")
        self.assertEqual(self.currency.symbol, "$")

class CurrencyExchangeRateModelTestCase(TestCase):
    def setUp(self):
        self.currency_usd = Currency.objects.create(code="USD", name="US Dollar", symbol="$")
        self.currency_eur = Currency.objects.create(code="EUR", name="Euro", symbol="€")
        self.exchange_rate = CurrencyExchangeRate.objects.create(
            source_currency=self.currency_usd,
            exchanged_currency=self.currency_eur,
            valuation_date=datetime.now().date(),
            rate_value=1.1
        )

    def test_exchange_rate_creation(self):
        self.assertEqual(self.exchange_rate.source_currency.code, "USD")
        self.assertEqual(self.exchange_rate.exchanged_currency.code, "EUR")
        self.assertAlmostEqual(self.exchange_rate.rate_value, 1.1, places=6)


class ExchangeRateServiceTestCase(TestCase):
    def setUp(self):
        self.mock_provider = "mock"

    @patch("currency.services.get_exchange_rate_data")
    def test_get_exchange_rate_data_success(self, mock_get_data):
        mock_get_data.return_value = 1.2
        rate = get_exchange_rate_data("USD", "EUR", "2023-11-01", self.mock_provider)
        self.assertEqual(rate, 1.2)

    @patch("currency.services.get_exchange_rate_data")
    def test_get_exchange_rate_data_failure(self, mock_get_data):
        mock_get_data.return_value = None
        rate = get_exchange_rate_data("USD", "EUR", "2023-11-01", self.mock_provider)
        self.assertIsNone(rate)


class CurrencyCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.currency_data = {"code": "USD", "name": "US Dollar", "symbol": "$"}
        self.currency = Currency.objects.create(**self.currency_data)

    def test_create_currency(self):
        response = self.client.post("/api/currencies/", self.currency_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code"], "USD")

    def test_list_currencies(self):
        response = self.client.get("/api/currencies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_currency(self):
        response = self.client.put(f"/api/currencies/{self.currency.id}/", {"name": "Updated US Dollar"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated US Dollar")

    def test_delete_currency(self):
        response = self.client.delete(f"/api/currencies/{self.currency.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ExchangeRateListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.currency_usd = Currency.objects.create(code="USD", name="US Dollar", symbol="$")
        self.currency_eur = Currency.objects.create(code="EUR", name="Euro", symbol="€")
        CurrencyExchangeRate.objects.create(
            source_currency=self.currency_usd,
            exchanged_currency=self.currency_eur,
            valuation_date="2023-11-01",
            rate_value=1.1
        )

    def test_get_exchange_rates(self):
        response = self.client.get("/api/exchange-rates/", {"source_currency": "USD", "date_from": "2023-11-01", "date_to": "2023-11-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["rate_value"], "1.100000")


class CurrencyConverterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.currency_usd = Currency.objects.create(code="USD", name="US Dollar", symbol="$")
        self.currency_eur = Currency.objects.create(code="EUR", name="Euro", symbol="€")
        CurrencyExchangeRate.objects.create(
            source_currency=self.currency_usd,
            exchanged_currency=self.currency_eur,
            valuation_date=datetime.now().date(),
            rate_value=1.1
        )

    def test_currency_conversion(self):
        response = self.client.get("/api/convert/", {"source_currency": "USD", "amount": 100, "exchanged_currency": "EUR"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["converted_amount"], 110.0)

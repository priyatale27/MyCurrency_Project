import requests
from .base import BaseCurrencyAdapter
#from decouple import config
from django.conf import settings

class CurrencyBeaconAdapter(BaseCurrencyAdapter):
    API_KEY = settings.CURRENCY_BEACON_API_KEY
    BASE_URL = 'https://api.currencybeacon.com/v1'

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        url = f"{self.BASE_URL}/historical"
        params = {
            'api_key': self.API_KEY,
            'base': source_currency,
            'symbols': exchanged_currency,
            'date': valuation_date
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['rates'].get(exchanged_currency)
        return None

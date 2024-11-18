import random
from .base import BaseCurrencyAdapter

class MockCurrencyAdapter(BaseCurrencyAdapter):
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        return round(random.uniform(0.5, 1.5), 6)

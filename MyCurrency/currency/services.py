from .adapters.currency_beacon import CurrencyBeaconAdapter
from .adapters.mock import MockCurrencyAdapter

def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    adapters = {
        'currency_beacon': CurrencyBeaconAdapter(),
        'mock': MockCurrencyAdapter(),
    }
    adapter = adapters.get(provider)
    if adapter:
        return adapter.get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)
    raise ValueError("Invalid provider")

class BaseCurrencyAdapter:
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        raise NotImplementedError("Subclasses must override get_exchange_rate_data()")

from datetime import datetime, timedelta
from celery import shared_task
from .models import Currency, CurrencyExchangeRate
from .services import get_exchange_rate_data


@shared_task
def load_historical_data(start_date, end_date, provider="mock"):
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        currencies = Currency.objects.all()
        source_currencies = currencies.values_list('code', flat=True)

        current_date = start_date
        while current_date <= end_date:
            valuation_date = current_date.strftime('%Y-%m-%d')

            for source_currency in source_currencies:
                for target_currency in source_currencies:
                    if source_currency != target_currency:
                        rate = get_exchange_rate_data(
                            source_currency,
                            target_currency,
                            valuation_date,
                            provider
                        )

                        if rate:
                            CurrencyExchangeRate.objects.get_or_create(
                                source_currency=Currency.objects.get(code=source_currency),
                                exchanged_currency=Currency.objects.get(code=target_currency),
                                valuation_date=valuation_date,
                                defaults={'rate_value': rate}
                            )

            current_date += timedelta(days=1)

        return f"Historical data loaded for the range {start_date} to {end_date}"
    except Exception as e:
        return str(e)

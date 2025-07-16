import csv
from io import StringIO

import requests
from django.conf import settings
from django.core.cache import cache

from celery import shared_task


@shared_task
def refresh_bitcoin_rates():
    resp = requests.get(settings.BITCOIN_TICKER_URL)
    rates = resp.json()
    for currency, rate in rates.items():
        cache.set(f"bitcoin_rate_{currency}", rate["last"], None)


@shared_task
def refresh_exchange_rates():
    currencies = "+".join(settings.EXCHANGE_RATE_CURRENCIES)
    url = settings.EXCHANGE_RATE_URL.format(
        currencies=currencies, base_currency=settings.EXCHANGE_RATE_BASE_CURRENCY
    )
    headers = {"Accept": "text/csv"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)
        for row in reader:
            cache.set(f"exchange_rate_{row['CURRENCY']}", float(row["OBS_VALUE"]), None)
        cache.set(f"exchange_rate_{settings.EXCHANGE_RATE_BASE_CURRENCY}", 1.0, None)
    else:
        raise Exception(
            f"Failed to retrieve exchange rates: HTTP {response.status_code}"
        )

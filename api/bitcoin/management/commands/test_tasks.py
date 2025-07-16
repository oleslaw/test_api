import time

from django.core.cache import cache
from django.core.management.base import BaseCommand

from api.bitcoin.tasks import refresh_bitcoin_rates, refresh_exchange_rates


class Command(BaseCommand):
    help = "Test Bitcoin and Exchange Rate tasks"

    def handle(self, *args, **options):
        cache.delete("bitcoin_rate_USD")
        cache.delete("exchange_rate_USD")

        self.stdout.write("queueing Bitcoin rate task...")
        refresh_bitcoin_rates.delay()

        self.stdout.write("queueing exchange rate task...")
        refresh_exchange_rates.delay()

        time.sleep(5)

        bitcoin_rate = cache.get("bitcoin_rate_USD")
        self.stdout.write(f"Bitcoin USD rate: {bitcoin_rate}")

        exchange_rate = cache.get("exchange_rate_USD")
        self.stdout.write(f"USD/EUR exchange rate: {exchange_rate}")

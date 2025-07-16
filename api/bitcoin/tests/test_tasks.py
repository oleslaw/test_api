from unittest.mock import MagicMock, patch

from django.test import TestCase

from api.bitcoin import tasks


class BitcoinTasksTests(TestCase):
    def test_refresh_bitcoin_rates(self):
        mock_rates = {"USD": {"last": 30000}, "EUR": {"last": 27000}}
        with patch("api.bitcoin.tasks.requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_rates
            with patch("api.bitcoin.tasks.settings") as mock_settings:
                mock_settings.BITCOIN_TICKER_URL = "http://fake-url"
                with patch("api.bitcoin.tasks.cache.set") as mock_cache_set:
                    tasks.refresh_bitcoin_rates()
                    mock_cache_set.assert_any_call("bitcoin_rate_USD", 30000, None)
                    mock_cache_set.assert_any_call("bitcoin_rate_EUR", 27000, None)

    def test_refresh_exchange_rates(self):
        mock_csv = "CURRENCY,OBS_VALUE\nUSD,1.1\nEUR,0.9\n"
        with patch("api.bitcoin.tasks.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = mock_csv
            mock_get.return_value = mock_response
            with patch("api.bitcoin.tasks.settings") as mock_settings:
                mock_settings.EXCHANGE_RATE_CURRENCIES = ["USD", "EUR"]
                mock_settings.EXCHANGE_RATE_URL = (
                    "http://fake-url?currencies={currencies}&base={base_currency}"
                )
                mock_settings.EXCHANGE_RATE_BASE_CURRENCY = "USD"
                with patch("api.bitcoin.tasks.cache.set") as mock_cache_set:
                    tasks.refresh_exchange_rates()
                    mock_cache_set.assert_any_call("exchange_rate_USD", 1.1, None)
                    mock_cache_set.assert_any_call("exchange_rate_EUR", 0.9, None)
                    mock_cache_set.assert_any_call("exchange_rate_USD", 1.0, None)

    def test_refresh_exchange_rates_failure(self):
        with patch("api.bitcoin.tasks.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            with patch("api.bitcoin.tasks.settings") as mock_settings:
                mock_settings.EXCHANGE_RATE_CURRENCIES = ["USD", "EUR"]
                mock_settings.EXCHANGE_RATE_URL = (
                    "http://fake-url?currencies={currencies}&base={base_currency}"
                )
                mock_settings.EXCHANGE_RATE_BASE_CURRENCY = "USD"
                with self.assertRaises(Exception) as context:
                    tasks.refresh_exchange_rates()
                self.assertIn(
                    "Failed to retrieve exchange rates: HTTP 404",
                    str(context.exception),
                )

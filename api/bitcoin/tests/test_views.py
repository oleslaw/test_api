from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.bitcoin.views import BitcoinConversionView


class BitcoinConversionViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse("bitcoin-convert")

    def test_bitcoin_conversion_success(self):
        request = self.factory.get(
            self.url, {"source_currency": "USD", "target_currency": "EUR"}
        )
        with patch("api.bitcoin.views.ConvertSerializer") as mock_serializer:
            mock_serializer.return_value.is_valid.return_value = True
            mock_serializer.return_value.validated_data = {
                "source_currency": "USD",
                "target_currency": "EUR",
            }
            with patch("api.bitcoin.views.cache.get") as mock_cache_get:
                mock_cache_get.side_effect = [30000, 1.0, 0.9]
                view = BitcoinConversionView.as_view()
                response = view(request)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                data = response.data
                self.assertEqual(data["bitcoin_price"], 30000)
                self.assertEqual(data["exchange_rate"], 0.9)
                self.assertEqual(data["converted_price"], 27000)

    def test_bitcoin_conversion_missing_rates(self):
        request = self.factory.get(
            self.url, {"source_currency": "USD", "target_currency": "EUR"}
        )
        with patch("api.bitcoin.views.ConvertSerializer") as mock_serializer:
            mock_serializer.return_value.is_valid.return_value = True
            mock_serializer.return_value.validated_data = {
                "source_currency": "USD",
                "target_currency": "EUR",
            }
            with patch("api.bitcoin.views.cache.get") as mock_cache_get:
                mock_cache_get.side_effect = [None, 1.0, 0.9]
                view = BitcoinConversionView.as_view()
                response = view(request)
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertIn("error", response.data)

    def test_bitcoin_conversion_invalid_params(self):
        request = self.factory.get(self.url, {"source_currency": "USD"})
        with patch("api.bitcoin.views.ConvertSerializer") as mock_serializer:
            mock_serializer.return_value.is_valid.return_value = False
            mock_serializer.return_value.errors = {
                "target_currency": ["This field is required."]
            }
            view = BitcoinConversionView.as_view()
            response = view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("target_currency", response.data)

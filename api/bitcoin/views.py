from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ConvertSerializer


class BitcoinConversionView(APIView):
    def get(self, request):
        serializer = ConvertSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        source = serializer.validated_data["source_currency"]
        target = serializer.validated_data["target_currency"]

        bitcoin_price = cache.get(f"bitcoin_rate_{source}")
        rate_source = cache.get(f"exchange_rate_{source}")
        rate_target = cache.get(f"exchange_rate_{target}")
        if bitcoin_price is None or rate_source is None or rate_target is None:
            return Response(
                {"error": "Rates not available"}, status=status.HTTP_404_NOT_FOUND
            )

        exchange_rate = rate_target / rate_source
        converted_price = bitcoin_price * exchange_rate

        return Response(
            {
                "bitcoin_price": bitcoin_price,
                "exchange_rate": exchange_rate,
                "converted_price": converted_price,
            }
        )

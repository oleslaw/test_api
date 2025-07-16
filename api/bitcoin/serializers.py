from rest_framework import serializers


class ConvertSerializer(serializers.Serializer):
    source_currency = serializers.ChoiceField(
        choices=["EUR", "GBP", "USD", "JPY", "CHF", "AUD"]
    )
    target_currency = serializers.ChoiceField(
        choices=["EUR", "GBP", "USD", "JPY", "CHF", "AUD"]
    )

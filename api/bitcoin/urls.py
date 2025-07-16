from django.urls import path

from .views import BitcoinConversionView

urlpatterns = [
    path("convert/", BitcoinConversionView.as_view(), name="bitcoin-convert"),
]

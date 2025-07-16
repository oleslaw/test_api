from django.urls import path

from .views import ContactImportView

urlpatterns = [
    path("import/", ContactImportView.as_view(), name="contact-import"),
]

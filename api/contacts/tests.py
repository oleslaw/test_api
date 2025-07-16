from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Contact


class ContactModelTest(TestCase):
    def test_str_method(self):
        contact = Contact.objects.create(
            first_name="Jan",
            last_name="Kowalski",
            email="jan.kowalski@example.com",
            phone="1234567890",
        )
        self.assertEqual(str(contact), "Jan Kowalski <jan.kowalski@example.com>")


class ContactImportViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("contact-import")

    def _make_csv(self, rows):
        header = "first_name,last_name,email,phone\n"
        data = "".join(
            [
                f"{r['first_name']},{r['last_name']},{r['email']},{r['phone']}\n"
                for r in rows
            ]
        )
        return header + data

    def test_import_valid_contacts(self):
        csv_content = self._make_csv(
            [
                {
                    "first_name": "Alice",
                    "last_name": "Smith",
                    "email": "alice@example.com",
                    "phone": "111",
                },
                {
                    "first_name": "Bob",
                    "last_name": "Brown",
                    "email": "bob@example.com",
                    "phone": "222",
                },
            ]
        )
        file = SimpleUploadedFile(
            "contacts.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )
        response = self.client.post(self.url, {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)

    def test_import_invalid_contacts(self):
        csv_content = self._make_csv(
            [
                {
                    "first_name": "",
                    "last_name": "Smith",
                    "email": "not-an-email",
                    "phone": "111",
                }
            ]
        )
        file = SimpleUploadedFile(
            "contacts.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )
        response = self.client.post(self.url, {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertEqual(Contact.objects.count(), 0)

    def test_import_no_file(self):
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

from django.db import transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contact
from .parsers import parse_contacts_csv
from .serializers import ContactSerializer


class ContactImportView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            rows = parse_contacts_csv(file)
        except Exception as e:
            return Response(
                {"error": f"Invalid CSV file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        contacts_to_create = []
        errors = []
        for idx, row in enumerate(rows, start=1):
            serializer = ContactSerializer(data=row)
            if serializer.is_valid():
                contacts_to_create.append(Contact(**serializer.validated_data))
            else:
                errors.append({"row": idx, "errors": serializer.errors, "data": row})

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                Contact.objects.bulk_create(contacts_to_create)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"imported": len(contacts_to_create)}, status=status.HTTP_201_CREATED
        )

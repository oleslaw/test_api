from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create initial users"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "Xyq4Q4C3UT")
            self.stdout.write(self.style.SUCCESS("Admin user created."))
        else:
            self.stdout.write("Admin user already exists.")
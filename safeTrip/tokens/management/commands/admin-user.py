from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="aditya-admin").exists():
            User.objects.create_superuser("aditya-admin", "aditya.bhimesh@gmail.com", "admin")
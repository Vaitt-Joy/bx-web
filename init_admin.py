import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BxWeb.settings")
django.setup()

from django.contrib.auth.models import User

try:
    admin = User.objects.get(username='viczhou')
except:
    User.objects.create_superuser('viczhou', 'tom@example.com', 'android123')

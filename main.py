import sys, os
sys.dont_write_bytecode = True

# django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from db.models import *

from django.urls import path
from decouple import config
from . import views


urlpatterns = [
    path(config("BOT_TOKEN"), views.hook),
]

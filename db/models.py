from django.db import models


class User(models.Model):
    chat_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=15, blank=True)
    middle_name = models.CharField(max_length=15, blank=True)
    pages = models.JSONField(null=True)


class Page(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    last_update = models.IntegerField()
    subscribers = models.TextField(default='[]')
    is_facebook = models.BooleanField(default=True)

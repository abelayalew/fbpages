from django.db import models


class User(models.Model):
    chat_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=15, blank=True)
    middle_name = models.CharField(max_length=15, blank=True)
    username = models.CharField(max_length=20, blank=True)
    pages = models.TextField(default='{}')

    def __str__(self):
        return str(self.chat_id)


class Page(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    last_update = models.BigIntegerField(blank=True, null=True)
    subscribers = models.TextField(default='[]')
    is_facebook = models.BooleanField(default=True)

    def __str__(self):
        return self.name

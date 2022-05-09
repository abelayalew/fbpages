from django.db import models

class TelegramUser(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    
    username = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)


class FacebookPage(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    last_update = models.BigIntegerField(blank=True)
    subscribers = models.ManyToManyField(TelegramUser, related_name='subscribers')

    def __str__(self):
        return self.name
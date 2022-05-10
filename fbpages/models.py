from django.db import models

class TelegramUser(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    
    username = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    
    @classmethod
    def from_telegram_update(cls, update):
        try:
            user = cls.objects.get(id=update.effective_user.id)
        except cls.DoesNotExist:
            user = cls(
                id=update.effective_user.id,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name,
                username=update.effective_user.username,    
            )
            user.save()
        
        return user


class FacebookPage(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    last_update = models.BigIntegerField(blank=True, null=True)
    subscribers = models.ManyToManyField(TelegramUser, related_name='subscriptions')

    def __str__(self):
        return self.name
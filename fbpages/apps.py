from django.apps import AppConfig
from decouple import config
from telegram import Bot
from telegram.ext import Updater

class FbpagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fbpages'

    def ready(self):
        from . import util

        hook_url = f'{config("HOOK_URL")}/{config("BOT_TOKEN")}'
        
        bot = Bot(config('BOT_TOKEN'))

        if bot.get_webhook_info().url != hook_url:
            bot.setWebhook(url=hook_url)
        
        updater = Updater(config('BOT_TOKEN'))
        
        util.DISPATCHER = updater.dispatcher
        util.BOT = bot

        from .tgbot import MainBot
        MainBot(util.DISPATCHER)
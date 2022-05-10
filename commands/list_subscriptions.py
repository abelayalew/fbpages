from telegram.ext import CallbackContext
from telegram import Update
from fbpages import models


def list_subscriptions(update: Update, context: CallbackContext):
    user = models.TelegramUser.from_telegram_update(update)
    
    text = "Your Subscriptions:\n"
    
    for page in user.subscriptions.all():
        text += f"{page.name}\n"
    
    update.effective_message.reply_text(text)
    
    
from telegram.ext import CallbackContext
from telegram import Update
from fbpages import models
from facebook_scraper import get_posts
from requests.exceptions import HTTPError

def add(update: Update, context: CallbackContext):
    user = models.TelegramUser.from_telegram_update(update)
    page_name = update.effective_message.text.split(' ')[1]
    
    if page_name.__contains__('/'):
        page_name = page_name.split('/')[-1]
    
    try:
        page = models.FacebookPage.objects.get(name=page_name)
        page.subscribers.add(user)
        update.effective_message.reply_text("Successfully Added!")
        return
    except models.FacebookPage.DoesNotExist:
        pass
    
    try:
        posts = list(get_posts(page_name, pages=1))
        
        if not posts:
            update.effective_message.reply_text("Page Not Found!")
            return
        
        page = models.FacebookPage(name=page_name)
        page.save()
        page.subscribers.add(user)
        
        update.effective_message.reply_text("Successfully Added!")
        # page.save()
     
    except HTTPError:
        update.effective_message.reply_text("Make Sure The Page Exists!")   
    
    
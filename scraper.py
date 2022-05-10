import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
import django
django.setup()

from fbpages import models
from facebook_scraper import get_posts
from telegram import Bot, ParseMode
from decouple import config

bot = Bot(config('BOT_TOKEN'))


for page in models.FacebookPage.objects.all():
    subscribers = page.subscribers.all()
    
    for post in get_posts(page.name, pages=3):
        if page.last_update and page.last_update > int(post['post_id']):
            continue
        
        page.last_update = int(post['post_id'])
        
        text = f"#{page.name}\n\n" + post['post_text'][:800] + f"\n\n<a href='{post['post_url']}'>click here to read more</a>"
        
        for subscriber in subscribers:
            
            if post['image']:
                bot.sendPhoto(chat_id=subscriber.id, photo=post['image'], caption=text, parse_mode=ParseMode.HTML)
            
            else:
                bot.sendMessage(chat_id=subscriber.id, text=text, parse_mode=ParseMode.HTML)
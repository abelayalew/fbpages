from fbpages import models
from facebook_scraper import get_posts
from telegram import Bot
from decouple import config


bot = Bot(config('BOT_TOKEN'))


for page in models.FacebookPage.objects.all():
    subscribers = page.subscribers.all()
    
    for post in get_posts(page.name, pages=3):
        if page.last_update and page.last_update > int(post['post_id']):
            continue
        
        page.last_update = int(post['post_id'])
        
        text = f"#{page.name}\n\n" + post['post_text'][:800]
        
        for subscriber in subscribers:
            
            if post['image']:
                bot.sendPhoto(chat_id=subscriber.id, photo=post['image'], caption=text)
            
            else:
                bot.sendMessage(chat_id=subscriber.id, text=text)
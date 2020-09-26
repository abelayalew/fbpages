import time
import telegram
import threading
from facebook_scraper import get_posts
from db.models import *
from decouple import config
TOKEN = config('TOKEN')


def post_handler(page, bot):
    name = page.name
    subscribers = eval(page.subscribers)

    for post in get_posts(name, pages=1, youtube_dl=True):
        try:
            for chat_id in subscribers:
                link = post["post_url"]
                if post['image']:
                    text = f'#{name[:13]}\n\n{post["text"][:983]}\n\nClick <a href="{link}">Here</a> for more ...'
                    bot.sendPhoto(chat_id=chat_id, photo=post['image'], caption=text, parse_mode=telegram.ParseMode.HTML)

                elif post['video']:
                    print('video found')

                else:
                    text = f'#{name[:13]}\n\n{post["text"][:983]}\n\nClick <a href="{link}">Here</a> for more ...'
                    bot.sendMessage(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML)

        except Exception as e:
            print(f"Exception Occurred - {e}")


def post_threader():
    bot = telegram.Bot(TOKEN)
    while True:
        for page in Page.objects.all():
            print(page)
            threading.Thread(target=post_handler, args=(page, bot)).start()
        time.sleep(200)


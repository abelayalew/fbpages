import time, os
import telegram
import threading
from facebook_scraper import get_posts
from db.models import *
from decouple import config
import youtube_dl as yt
import random, string

TOKEN = config('TOKEN')


def fb_post_handler(page, bot):
    name = page.name
    subscribers = eval(page.subscribers)
    if not subscribers:
        page.delete()
        return
    posts = []
    for post in get_posts(name, pages=1, youtube_dl=True):
        try:
            int(post['post_id'])  # checking for valid posts, sometimes None gets here
            posts.append(post)
        except Exception as e:
            print(f"Exception Caught - {e}")

    for post in sorted(posts, key=lambda t: t['post_id']):
        last_update = page.last_update
        if int(post['post_id']) > last_update:
            page.last_update = int(post['post_id'])
            page.save()
        else:
            continue
        try:
            for chat_id in subscribers:
                link = post["post_url"]
                video = None
                if post['image']:
                    text = f'#{name[:13]}\n\n{post["text"][:983]}\n\nClick <a href="{link}">Here</a> for more ...'
                    bot.sendPhoto(chat_id=chat_id, photo=post['image'], caption=text, parse_mode=telegram.ParseMode.HTML)

                elif post['video']:
                    text = f'#{name[:13]}\n\n{post["text"][:983]}\n\nClick <a href="{link}">Here</a> for more ...'
                    if video:
                        bot.sendVideo(chat_id=chat_id, video=video, caption=text,
                                      parse_mode=telegram.ParseMode.HTML)
                        continue

                    try:
                        title = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                        ydl_opts = {
                            'outtmpl': f"{title}.mp4",
                            'postprocessors': [{
                                'key': 'FFmpegVideoConvertor',
                                'preferedformat': 'mp4',  # one of avi, flv, mkv, mp4, ogg, webm
                            }],
                        }
                        with yt.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([post['video']])

                        v = bot.sendVideo(chat_id=chat_id,
                                          video=open(f'{title}.mp4', 'rb'),
                                          caption=text,
                                          parse_mode=telegram.ParseMode.HTML)
                        video = v.video

                    except Exception as e:
                        print(f"Exception Caught - {e}")
                try:
                    for i in os.listdir():
                        if i.split('.')[-1] == 'mp4':
                            os.remove(i)
                except:
                    pass

                else:
                    text = f'#{name[:13]}\n\n{post["text"][:983]}\n\nClick <a href="{link}">Here</a> for more ...'
                    bot.sendMessage(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML)

        except Exception as e:
            print(f"Exception Occurred - {e}")


def post_threader():
    bot = telegram.Bot(TOKEN)
    while True:
        for page in Page.objects.all():
            threading.Thread(target=fb_post_handler, args=(page, bot)).start()
        time.sleep(300)

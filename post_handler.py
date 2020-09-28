import time, os
import telegram
import threading
from facebook_scraper import get_posts
from db.models import *
import youtube_dl as yt
import random, string
import re

TOKEN = os.environ.get('TOKEN')


def fb_post_handler(page, bot):
    name = page.name
    subscribers = eval(page.subscribers)
    if not subscribers:
        page.delete()
        return
    posts = []
    for post in get_posts(name, pages=5, youtube_dl=True):
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
                    # adding youtube support
                    try:
                        link = re.search("(?P<url>https?://[^\s]+)", text).group("url")
                        title = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                        ydl_opts = {
                            'outtmpl': f"{title}.mp4",
                            'postprocessors': [{
                                'key': 'FFmpegVideoConvertor',
                                'preferedformat': 'mp4',  # one of avi, flv, mkv, mp4, ogg, webm
                            }],
                        }
                        with yt.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([link])

                        bot.sendVideo(chat_id=chat_id,
                                          video=open(f'{title}.mp4', 'rb'),
                                          caption=text,
                                          parse_mode=telegram.ParseMode.HTML)
                        continue
                    except:
                        pass

                    bot.sendPhoto(chat_id=chat_id, photo=post['image'], caption=text, parse_mode=telegram.ParseMode.HTML)
                    continue

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
                        continue

                    except Exception as e:
                        print(f"Exception Caught - {e}")
                        continue

                else:
                    text = f'#{name[:13]}\n\n{post["text"][:983]}\n\nClick <a href="{link}">Here</a> for more ...'
                    # adding youtube support
                    try:
                        link = re.search("(?P<url>https?://[^\s]+)", text).group("url")
                        title = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                        ydl_opts = {
                            'outtmpl': f"{title}.mp4",
                            'postprocessors': [{
                                'key': 'FFmpegVideoConvertor',
                                'preferedformat': 'mp4',  # one of avi, flv, mkv, mp4, ogg, webm
                            }],
                        }
                        with yt.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([link])

                        bot.sendVideo(chat_id=chat_id,
                                      video=open(f'{title}.mp4', 'rb'),
                                      caption=text,
                                      parse_mode=telegram.ParseMode.HTML)
                        continue
                    except:
                        pass

                    bot.sendMessage(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML)

                try:
                    for i in os.listdir():
                        if i.split('.')[-1] == 'mp4':
                            os.remove(i)
                except:
                    pass

        except Exception as e:
            print(f"Exception Occurred - {e}")


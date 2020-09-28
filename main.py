# -*- coding: utf-8 -*-
import sys, os
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from facebook_scraper import get_posts
import threading, time, telegram, requests

# django setup
sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from commands import Add, Help, List, Remove, Start
import post_handler
from db.models import *

# tokens
TOKEN = os.environ.get('TOKEN')
URL = os.environ.get('URL')
BRO_URL = os.environ.get('BRO_URL')  # twin bot that works in shift on heroku
PORT = int(os.environ.get('PORT', 5000))
BOT_ID = os.environ.get('BOT_ID')


class FbPage:
    def __init__(self):
        self.start_time = time.time()
        self.updater = Updater(token=TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start_bot(self):
        """
        start the bot
        :return: None
        """
        self.dispatcher.add_handler(MessageHandler(Filters.command, self.command_handler))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.text_handler))
        self.dispatcher.add_handler(CallbackQueryHandler(Remove.callbacks))
        self.updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
        self.updater.bot.setWebhook(URL + TOKEN)
        threading.Thread(target=self.main_loop).start()
        print("Initialized")

    def main_loop(self):
        bot = telegram.Bot(TOKEN)
        for i in range(12):
            requests.request('GET', URL)
            bot.sendMessage(chat_id=1042037718, text=f'round {i}')
            for page in Page.objects.all():
                threading.Thread(target=post_handler.fb_post_handler, args=(page, bot)).start()
            time.sleep(300)

        while (time.time() - self.start_time) < 1800:
            for page in Page.objects.all():
                threading.Thread(target=post_handler.fb_post_handler, args=(page, bot)).start()
            time.sleep(300)
        self.updater.stop()
        requests.request('GET', BRO_URL)
        print('ping sent to brother')

    def extract_message(self, update):
        chat_id = update.message.chat_id  # 0
        first_name = update.message.chat.first_name  # 1
        last_name = update.message.chat.last_name  # 2
        username = update.message.chat.username  # 3
        message = update.message.text  # 4
        message_id = update.message.message_id  # 5
        print(chat_id, first_name, last_name, username, message, message_id)
        return chat_id, first_name, last_name, username, message, message_id

    def command_handler(self, update, context) -> None:
        """
        a method to handle all commands
        :param update:
        :param context:
        :return: None
        """
        self.start_time = time.time()
        command = update.message.text.split(' ')[0]
        supported_commands = {
            '/start': Start.command_start,
            '/add': Add.command_add,
            '/help': Help.command_help,
            '/list': List.command_list,
            '/remove': Remove.command_remove
        }
        if command in supported_commands:
            supported_commands[command](update, context, *self.extract_message(update))
        elif 'remove' in command:
            Remove.command_remove(update, context)

    def text_handler(self, update, context):
        """
        https://www.facebook.com/pagename/adss
        https://m.facebook.com/pagename/adss

        :param update:
        :param context:
        :return:
        """
        data = list(self.extract_message(update))
        text = update.message.text
        if 'facebook.com' in text:
            self.start_time = time.time()
            try:
                page = text.split('facebook.com')[1].split('/')[1]
                list(get_posts(page, pages=1))
                data.append(page)
                Add.command_add(update, context, *tuple(data))
                return
            except:
                update.message.reply_text("Invalid Link or Can't Add That Page.")
                return
        elif text == '.status':
            update.message.reply_text(f"{BOT_ID}\n{(time.time() - self.start_time)//60} Minutes.")
            self.start_time = time.time()
            return
        self.start_time = time.time()
        update.message.reply_text("Unrecognized Text")
        self.start_time = time.time()


bot = FbPage()
bot.start_bot()

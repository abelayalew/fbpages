from telegram.ext import Dispatcher, CommandHandler

class MainBot:
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.dispatcher.add_handler(CommandHandler('start', self.start))
    
    def start(self, update, context):
        update.message.reply_text("Hello!")
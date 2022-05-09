from telegram.ext import Dispatcher, CommandHandler
from commands import add
class MainBot:
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.update_handlers()
        
    def update_handlers(self):
        self.dispatcher.add_handler(CommandHandler('add', add.add))
        
    def start(self, update, context):
        update.message.reply_text("Hello!")
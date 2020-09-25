from db.models import *


def command_start(update, context, *args):
    bot = context.bot
    chat_id = update.message.chat_id

    try:
        User.objects.get(chat_id=chat_id)
    except User.DoesNotExist:
        User.objects.create(
            chat_id=args[0], first_name=args[1] or "", middle_name=args[2] or "", username=args[3] or ""
        )
    greeting = f"Hello {args[1]} !\nWelcome To FbPages.\n\nfor more details use the /help menu."
    bot.sendMessage(chat_id=chat_id, text=greeting)

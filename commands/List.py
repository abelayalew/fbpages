from db.models import *


def command_list(update, context, *args):
    reply_list = "Your Facebook Page Subscriptions :\n"
    pages = eval(User.objects.get(chat_id=args[0]).pages)
    pages.insert(0, 0)
    print(pages)
    for i in range(1, len(pages)):
        reply_list += f"{i}. {pages[i]}\n"

    update.message.reply_text(reply_list)
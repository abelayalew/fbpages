from db.models import *


def command_list(update, context, *args):
    reply_list = "Your Facebook Page Subscriptions :\n"
    pages: dict = eval(User.objects.get(chat_id=args[0]).pages)
    if not pages:
        update.message.reply_text("You Dont Have Any Subscriptions.")
        return
    counter = 1
    for name in pages:
        db_page = Page.objects.get(name=name)
        if db_page.is_facebook:
            reply_list += f"{counter}. fb - {pages[name] or name}\n"
        else:
            reply_list += f"{counter}. tw - {pages[name] or name}\n"
        counter += 1

    update.message.reply_text(reply_list)

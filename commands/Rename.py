from db.models import *


def rename_page(update, context, *args):
    user = User.objects.get(chat_id=args[0])
    _, index, custom_name = int(args[4].split(' ')[1])
    try:
        index = int(index)
    except:
        update.message.reply_text("Invalid Command Usage, \n\nSee /help for more")
    if len(custom_name) > 15:
        update.message.reply_text("Custom Name Can't Exceed 15 Characters")
        return
    user_page: dict = eval(user.pages)
    if len(user_page) < index:
        update.message.reply_text("Index Exceeded Your Number Of Subscriptions")
        return
    if not index:
        update.message.reply_text("Invalid Index")
    page = [0, *list(user_page.keys())][index]
    user_page[page] = custom_name
    user.pages = user_page
    user.save()
    update.message.reply_text(f"You Have Successfully Renamed Page '{page}' to {custom_name}")
    return

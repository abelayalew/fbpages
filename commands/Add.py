from db.models import *
from facebook_scraper import get_posts


def command_add(update, context, *args):
    user = User.objects.get(chat_id=args[0])
    user_pages: dict = eval(user.pages)

    if len(args) == 7:
        page = args[-1].lower()
    else:
        try:
            page = update.message.text[5:].lower()
            if page in user_pages.keys():
                update.message.reply_text(f"Page '{page}' Already Exist")
                return
            list(get_posts(page, pages=1))
        except:
            update.message.reply_text("Page Does Not Exist")
            return
    if page not in user_pages.keys():
        user_pages[page] = None
        user.pages = user_pages
        user.save()
    else:
        update.message.reply_text(f"Page '{page}' Already Exist")
        return

    try:
        db_page = Page.objects.get(name=page)
        subscribers: list = eval(db_page.subscribers)
        subscribers.append(args[0])
        db_page.save()
    except Page.DoesNotExist:
        Page.objects.create(name=page, last_update=0, subscribers=[args[0]])

    update.message.reply_text(f"Page {page} Added Successfully!\n\nSee Your Pages With /list")




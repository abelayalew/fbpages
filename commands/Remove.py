# -*- coding: utf-8 -*-
from db.models import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.core.paginator import Paginator


def pages_keyboard(user, page_number) -> tuple:
    user = User.objects.get(chat_id=user)
    user_pages: dict = eval(user.pages)
    paginated_pages = Paginator(list(user_pages.keys()), 10)  # only the fb names
    keyboard = []
    current = paginated_pages.page(page_number)

    for i in current.object_list:
        db_page = Page.objects.get(name=i)
        if db_page.is_facebook:
            if user_pages[i]:
                text = 'fb - ' + user_pages[i]
            else:
                text = 'fb - ' + i[:18]
        else:
            if user_pages[i]:
                text = 'tw - ' + user_pages[i]
            else:
                text = 'tw - ' + i[:18]
        keyboard.append([InlineKeyboardButton(text, callback_data=f"remove {text[5:]}")])
    if current.has_previous() and current.has_next():
        keyboard.append([
            InlineKeyboardButton("<< Prev", callback_data=f"prev {current.previous_page_number()}"),
            InlineKeyboardButton("Next >>", callback_data=f"next {current.next_page_number()}")
        ])
    elif current.has_previous():
        keyboard.append([InlineKeyboardButton("<< Prev", callback_data=f"prev {current.previous_page_number()}")])

    elif current.has_next():
        keyboard.append([InlineKeyboardButton("Next >>", callback_data=f"next {current.next_page_number()}")])
    keyboard.append([InlineKeyboardButton("Cancel", callback_data='cancel')])
    return keyboard, paginated_pages.num_pages


def command_remove(update, context, *args):
    # if remove have number in it transfer to remove with index (remove_index) function
    try:
        number = int(args[4].split(' ')[1])
        remove_index(update, context, args)
        return
    except:
        pass

    keyboard = pages_keyboard(args[0], 1)
    if len(keyboard[0]) == 1:  # keyboard only have cancel button
        update.message.reply_text("You Don't Have Pages To Remove.")
        return
    reply_markup = InlineKeyboardMarkup(keyboard[0])
    update.message.reply_text(f"Select The Page You Want To Remove\n\n\tPages 1 of {keyboard[1]}", reply_markup=reply_markup)


def remove_index(update, context, *args):
    user = User.objects.get(chat_id=args[0])
    try:
        index = int(args[4].split(' ')[1])
    except:
        update.message.reply_text("Invalid Command Usage, \n\nSee /help for more")
        return
    
    user_page: dict = eval(user.pages)
    if len(user_page) < index:
        update.message.reply_text("Index Exceeded Your Number Of Subscriptions")
        return
    if not index:
        update.message.reply_text("Invalid Index")
    page = [0, *list(user_page.keys())][index]
    del user_page[page]
    user.pages = user_page
    user.save()
    db_page = Page.objects.get(name=page)
    subscribers: list = eval(db_page.subscribers)
    subscribers.remove(args[0])
    db_page.subscribers = subscribers
    db_page.save()
    update.message.reply_text(f"You Have Successfully Unsubscribed From '{page}'")
    return


def callbacks(update, context, *args):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    if 'next' in query.data or 'prev' in query.data:
        page = int(query.data.split(' ')[1])
        keyboard = pages_keyboard(chat_id, page)
        reply_markup = InlineKeyboardMarkup(keyboard[0])
        query.edit_message_text(f"Select The Page You Want To Remove\n\n\tPages {page} of {keyboard[1]}", reply_markup=reply_markup)
    elif 'remove' in query.data:
        page = query.data.split(' ')[1]
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data=f"yes {page}"),
             InlineKeyboardButton("Hell No!", callback_data=f"cancel")]
        ]
        query.edit_message_text(f"Are You Sure You Want To Remove '{page}'",
                                reply_markup=InlineKeyboardMarkup(keyboard))
    elif 'yes' in query.data:
        removed = False
        page = query.data.split(' ')[1]
        user = User.objects.get(chat_id=chat_id)
        user_pages: dict = eval(user.pages)

        for _page in user_pages:
            if page == user_pages[_page]:
                del user_pages[_page]
                user.pages = user_pages
                user.save()
                removed = True
                break
            elif page in _page:
                del user_pages[_page]
                user.pages = user_pages
                user.save()
                removed = True
                break
        if not removed:
            query.edit_message_text("Page Not Found")
            return
        try:
            _page = page
            if page in user_pages.values():
                _page = user_pages[page]
            page_obj = Page.objects.get(name__startswith=_page)
            subscribers = eval(page_obj.subscribers)
            if chat_id in subscribers:
                subscribers.remove(chat_id)
            page_obj.subscribers = subscribers
            page_obj.save()
        except Page.DoesNotExist:
            pass
        query.edit_message_text(f"You Have Successfully Unsubscribed From '{page}'")
    elif 'cancel' in query.data:
        query.edit_message_text("Request Canceled!")

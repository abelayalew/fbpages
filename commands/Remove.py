# -*- coding: utf-8 -*-
from db.models import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.core.paginator import Paginator


def pages_keyboard(user, page) -> tuple:
    user = User.objects.get(chat_id=user)
    user_pages = Paginator(eval(user.pages), 5)
    keyboard = []
    current = user_pages.page(page)

    for i in current.object_list:
        keyboard.append([InlineKeyboardButton(i[:20].encode('utf-8'), callback_data=f"remove {i[:20].encode('utf-8')}")])
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
    return keyboard, user_pages.num_pages


def command_remove(update, context, *args):
    keyboard = pages_keyboard(args[0], 1)
    if len(keyboard[0]) == 1:
        update.message.reply_text("You Don't Have Pages To Remove.")
        return
    reply_markup = InlineKeyboardMarkup(keyboard[0])
    update.message.reply_text(f"Select The Page You Want To Remove\n\n\tPages 1 of {keyboard[1]}", reply_markup=reply_markup)


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
        remoed = False
        page = query.data.split(' ')[1]
        user = User.objects.get(chat_id=chat_id)
        user_pages = eval(user.pages)
        for _page in user_pages:
            if page in _page:
                user_pages.remove(_page)
                user.pages = user_pages
                user.save()
        if not remoed:
            query.edit_message_text("Page Not Found")
            return
        try:
            page_obj = Page.objects.get(name__startswith=page)
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

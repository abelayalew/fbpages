def command_help(update, context, *args):
    update.message.reply_text(text=open('commands/help.txt').read())

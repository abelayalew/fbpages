from django.http import JsonResponse
from telegram import Update, Bot
import json
from . import util
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def hook(request):
    data = json.loads(request.body.decode('UTF-8'))
    update = Update.de_json(data, util.BOT)

    util.DISPATCHER.process_update(update)
    return JsonResponse(data={}, status=200)
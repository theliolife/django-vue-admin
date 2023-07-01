from django.http import HttpResponse
import json
from django.http import JsonResponse, HttpResponse
from stock.models import Test
from datetime import datetime
from maotai.models import MtPrice

from libs.http_response import response

def index(request):
    return HttpResponse("茅台看板")


def get_list(request):
    name = request.GET.get('name')
    date_now = datetime.now().strftime("%Y-%m-%d")

    if name:
        data = MtPrice.getListByName(date_now, name)
    else:
        data = MtPrice.getList(date_now)

    # 或者直接使用JsonResponse函数
    return JsonResponse(response(data), safe=False, content_type="application/json")


def getBasic(request):
    email = request.GET.get('email')
    pass_word = request.GET.get('password')
    print(email, pass_word)

    data = {
        'name': email,
        'age': pass_word,
    }

    data = Test.getInfo()
    return JsonResponse(data, content_type="application/json")

from django.http import HttpResponse
import json
from django.http import JsonResponse, HttpResponse
from stock.models import Test

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def jsons(request):

    email = request.GET.get('email')
    pass_word = request.GET.get('password')
    print(email, pass_word)

    data = {
        'name': email,
        'age': pass_word,
    }

    #或者直接使用JsonResponse函数
    return JsonResponse(data, safe=False, content_type="application/json")


def getBasic(request):
    data = Test.getInfo()
    return JsonResponse(data, content_type="application/json")
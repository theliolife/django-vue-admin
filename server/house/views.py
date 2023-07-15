from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse, HttpResponse
from house.models import House
from datetime import datetime


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def dashboard(request):
    data = House.dashboard()
    res = {
        'code': 200,
        'data': data,
    }
    return JsonResponse(res, content_type="application/json")


def list(request):
    title = request.GET.get('title')
    floor = request.GET.get('floor')
    operate_time_start = request.GET.get('operate_time_start')
    operate_time_end = request.GET.get('operate_time_end')
    operate_date = request.GET.get('operate_date')
    if operate_date is None:
        # return JsonResponse({'data': "必须传递operate_date参数"}, content_type="application/json")
        operate_date = datetime.now().strftime("%Y-%m-%d")

    data = House.list(title, floor, operate_date)
    res = {
        'code': 200,
        'data': data,
    }
    return JsonResponse(res, content_type="application/json")

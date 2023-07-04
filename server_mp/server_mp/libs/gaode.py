# coding=utf-8

import os
import json
import requests

def routes(origin, destination):
    key = os.environ.get('GAO_DE_KEY')  ##输入自己key
    parameters = {'key': key, 'origin': origin, 'destination': destination}
    ##参数的输入，可以按照自己的需求选择出行时间最短，出行距离最短，不走高速等方案，结合自己需求设置，参考手册
    response = requests.get('https://restapi.amap.com/v3/direction/driving?parameters', params=parameters)
    text = json.loads(response.text)
    duration = text['route']['paths'][0]['duration']  ##出行时间
    ## 可以自己打印text看一下，能提取很多参数，出行时间、出行费用、出行花费等看自己需求提取

    return duration

# https://lbs.amap.com/api/webservice/guide/api/direction
def walks(origin, destination):
    key = os.environ.get('GAO_DE_KEY')  ##输入自己key
    parameters = {'key': key, 'origin': origin, 'destination': destination}
    ##参数的输入，可以按照自己的需求选择出行时间最短，出行距离最短，不走高速等方案，结合自己需求设置，参考手册
    response = requests.get('https://restapi.amap.com/v3/direction/walking?parameters', params=parameters)
    text = json.loads(response.text)
    duration = text['route']['paths'][0]['duration']  ##出行时间
    ## 可以自己打印text看一下，能提取很多参数，出行时间、出行费用、出行花费等看自己需求提取

    return duration
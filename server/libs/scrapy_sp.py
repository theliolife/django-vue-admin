from django.shortcuts import render

# Create your views here.
import requests


def get_status():
    # 获取状态
    url = "http://127.0.0.1:6800/daemonstatus.json"
    res = requests.get(url)
    return res.json()


def get_project_list():
    # 获取项目列表
    url = "http://127.0.0.1:6800/listprojects.json"
    res = requests.get(url)
    return res.json()


def get_spider_list(project):
    # 获取项目下已发布的爬虫列表
    url = "http://127.0.0.1:6800/listspiders.json?project={}".format(project)
    res = requests.get(url)
    return res.json()


def spider_list_ver(project):
    # 获取项目下已发布的爬虫版本列表
    url = "http://127.0.0.1:6800/listversions.json?project={}".format(project)
    res = requests.get(url)
    return res.json()


def get_spider_status(spider):
    # 获取爬虫运行状态
    url = "http://localhost:6800/listjobs.json?project={}".format(spider)
    res = requests.get(url)
    return res.json()


def start_spider(project, spider, kwargs=None):
    # 运行一个爬虫
    url = "http://localhost:6800/schedule.json"
    data = {
        "project": project,
        "spider": spider,
    }
    if kwargs:
        data["data"] = kwargs
    res = requests.post(url, data=data)
    return res.json()


def del_spider(project, version):
    # 删除某一版本爬虫
    url = "http://127.0.0.1:6800/delversion.json"
    data = {
        "project": project,
        "version": version,
    }
    res = requests.post(url, data=data)
    return res.json()


def del_pro(project):
    # 删除项目。注意：删除之前需要停止爬虫，才可以再次删除
    url = "http://127.0.0.1:6800/delproject.json"
    data = {
        "project": project,
    }
    res = requests.post(url, data=data)
    return res.json()


def get_jobs(project):
    # 获取jobs
    url = "http://127.0.0.1:6800/listjobs.json?project={}".format(project)
    res = requests.get(url)
    return res.json()


def cancel(project, job_id):
    # 取消job
    url = "http://localhost:6800/cancel.json"
    data = {
        "project": project,
        "job": job_id
    }
    res = requests.post(url, data=data)
    return res.json()


def publish():
    # 发布项目
    url = "http://127.0.0.1:6800/addversion.json"
    data = {
        "project": "mySpider",
        "version": 1,
        "egg": '1.egg'
    }
    res = requests.post(url, data=data)
    return res.json()
from django.http import HttpResponse
from django.shortcuts import render,redirect
import re


html_hello = """
<h5>hello world!</h>
<p>这是FCA主页</p>
"""


def hello(request):
    return HttpResponse(html_hello)


def index(request):
    """首页"""
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    print("ip:", ip)
    return render(request, "index.html")

'''
def register(request):
    """注册页面"""
    return render(request, "register.html")
'''


def login(request):
    """登录页面"""
    return render(request, "login.html")

def logout(request):
    """注销"""
    request.session.flush()
    return redirect('/')

def index2(request,name,student_number):
    return render(request, "index2.html",{"name":name})


def pages(request):
    """其他页面"""
    url = request.get_full_path()
    id_ = url.lstrip('/').split('.')
    print(url, id_)
    if id_[0] == '1':
        if id_[1] == '000':
            return render(request, "pages1/page_000.html")
    return None


def byUrl(request):
    """其他页面(通过路径访问)"""
    url = request.get_full_path()
    return render(request, url.lstrip('/'))

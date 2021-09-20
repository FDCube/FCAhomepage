from django.http import HttpResponse
from django.shortcuts import render, redirect
from database.models import Record
from FCAhomepage.core.utils import minute_to_sec, sec_to_minute
import re

EventList = ['三阶', '二阶', '四阶', '五阶', '六阶', '七阶', '单手', '三盲', '四盲', '金字塔', '斜转', 'SQ1','五魔方', '魔表', '最少步']

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


def record(request):
    events1 = []
    events = Record.objects.all()
    print(events)
    events = list(events)
    for i in EventList:
        for event in events:
            if event.cubeevent == i:
                event.time_average = sec_to_minute(event.time_average)
                event.time_single = sec_to_minute(event.time_single)
                events1.append(event)
    return render(request, 'record.html', {'events': events1})


def tutorial(request):
    return render(request, 'tutorial.html')

def event_start(request):
    if request.method == "POST" and request.POST:
        event_ = request.POST.get('event')
        round_ = request.POST.get('round')
        num_ = request.POST.get('num')
        if event_ is not None and round_ is not None and num_ is not None:
            round_ = int(round_)
            num_ = int(num_)
            # 获取对应打乱
            ...
        return render(request, 'compete_timer.html')
    return redirect('/competition')


def timer(request):
    return render(request, 'timer.html')



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

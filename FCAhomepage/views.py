from django.http import HttpResponse
from django.shortcuts import render


html_hello = """
<h5>hello world!</h>
<p>这是FCA主页</p>
"""


def hello(request):
    return HttpResponse(html_hello)


def index(request):
    return render(request, "index.html")

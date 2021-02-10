from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from database.models import Person,Competition,Competition
from .views import index2

def login_action(request):
    request.encoding = 'utf-8'
    # 获取输入的学号和密码
    student_number = request.GET.get('student_number')
    password = request.GET.get('passwd')
    # 发起查询
    line = Person.objects.filter(studentnumber=student_number)
    is_exist = 0
    real_passwd = None
    for var in line:
        is_exist = 1
        real_passwd = var.passwd  # 正确的密码
        name = var.name
    if is_exist == 0:  # 输入的学号不在数据库里
        return render(request, "login.html", {"student_number": student_number,"check1": "此学号还未注册！"})
    elif password != real_passwd:  # 密码不正确
        return render(request, "login.html", {"student_number": student_number, "check2": "输入的密码不正确！"})
    else:
        request.session['student_number'] = student_number
        request.session['name'] = name
        return redirect('/')
        return redirect(reverse('index2', kwargs={'name': name, 'student_number': student_number}))

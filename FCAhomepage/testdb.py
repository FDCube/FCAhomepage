# -*- coding: utf-8 -*-
# testdb是对数据库进行操作的测试，没有实际作用
from django.http import HttpResponse

from database.models import Login,Person,Competition,CompetitionTime


# 数据库操作
def testdb(request):
    # 初始化
    response = ""
    response1 = ""
    '''
    list = Person.objects.all()
    line = Person.objects.filter(passwd=123456)
    for var in line:
        student_no = var.studentnumber
    line2 = CompetitionTime.objects.filter(studentnumber=student_no)


    # 输出所有数据
    for var in line2:
        response1 += str(var.single_time) + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")
    '''
    line = Person.objects.filter(studentnumber=18307110137)
    line_change = Person.objects.get(studentnumber=18307110137)
    line_change.passwd = 12345
    line_change.save()
    line_change2 = Person(studentnumber=100, name='asdf', passwd=1111)
    line_change2.save()
    for var in line:
        response = str(var.passwd)

    return HttpResponse(response)


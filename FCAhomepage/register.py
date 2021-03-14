from django.http import HttpResponse
from django.shortcuts import render
from database.models import Person,Competition,CompetitionTime


# 表单
def register_form(request):
    return render(request, 'register.html')


# 接收请求数据
def register(request):
    request.encoding = 'utf-8'
    if request.method == "POST" and request.POST:
        student_number = request.POST.get('a')
        name = request.POST.get('b')
        college = request.POST.get('c')
        major = request.POST.get('d')
        passwd1 = request.POST.get('e')
        passwd2 = request.POST.get('f')
        wca_id = request.POST.get('g')

        '''
        if 'student_number' in request.GET and request.GET['student_number']:
            message = '你的学号为: ' + request.GET['student_number']
            return HttpResponse(request.GET['student_number'])
        '''
        # 先查找有没有重复学号
        line = Person.objects.filter(studentnumber=student_number)
        is_repeat = 0
        for var in line:
            is_repeat = 1

        if student_number != None and name != None and passwd1 != None and student_number != '' and name != '' and passwd1 != '' and passwd1 == passwd2 and is_repeat == 0:  # 如果满足所有条件，将注册信息写入数据库
            for i in [college,major,wca_id]:
                if i == '':
                    i = None
            line_register = Person(studentnumber=student_number, name=name, passwd=passwd1, major=major, college=college, wcaid=wca_id)
            line_register.save()
            return HttpResponse("success")
        else:  # 不满足条件
            if student_number != None:  # 学号右边的提示信息
                if student_number != '':
                    if is_repeat == 1:
                        return  HttpResponse("此学号已经注册过了！")
                    else:
                        return HttpResponse("")
                else:
                    message = '请输入学号'
                    return HttpResponse(message)

            elif name != None:  # 姓名右边的提示信息
                if name == '':
                    return HttpResponse('请输入姓名')
                else: return HttpResponse("")

            elif passwd1 != None and passwd2 != None:  # 判断两次输入的密码是否一样
                if passwd1 == "":
                    return HttpResponse("请输入密码")
                elif passwd1 != passwd2:
                    return HttpResponse('两次输入的密码不一样')
                else: return HttpResponse("")

        #return render(request,"register.html",{"output":message})
    else:
        return render(request, "login.html")
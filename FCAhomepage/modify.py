from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from database.models import Person,Competition,Competition

def modify(request):
    """修改个人信息页面，要在表单里显示个人信息"""
    student_number = request.session['student_number']
    name = request.session['name']
    # 发起查询
    line = Person.objects.filter(studentnumber=18307110137)
    for var in line:
        college = var.college  # 查询得到学院和专业
        major = var.major
        wca_id = var.wcaid

    return render(request, "modify.html", {"college": college, "major": major, 'wca_id':wca_id})

def modify_action(request):
    student_number = request.session['student_number']
    # 发起查询
    line = Person.objects.filter(studentnumber=student_number)
    for var in line:
        college = var.college  # 查询得到学院和专业
        major = var.major
    name = request.POST.get('name')
    college = request.POST.get('college')
    major = request.POST.get('major')
    wca_id = request.POST.get('wca_id')
    if name == '':  # 姓名为空
        return HttpResponse('empty')
    if college == '' or college == 'None':college = None
    if major == '' or major == 'None': major = None
    if wca_id == '' or wca_id == 'None': wca_id = None
    line.update(name=name, major=major, college=college, wcaid=wca_id)
    return HttpResponse("success")

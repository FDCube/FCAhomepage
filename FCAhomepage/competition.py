from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from database.models import Person,Competition,CompetitionTime
import datetime


def competition(request):
    student_number = request.session['student_number']
    eventlist = Competition.objects.all()
    eventlist = list(eventlist)  # 每个项目一个列表
    trans_list = []  # 传入前端的数组，需要重新生成
    row = 0
    for event in eventlist:
        signed = 0
        trans_list_element = []  # 表格的一行，包含名称，时间，状态，项目，操作
        start_time = event.competition_time
        start_time = start_time.replace(tzinfo=None)  # 转换为无时区时间，这样才能相减
        lasting_time = event.duration  # 获取比赛持续时间，分钟为单位
        now_time = datetime.datetime.now()
        real_duration=((now_time-start_time).days*86400+(now_time-start_time).seconds)/60  # 现在时间与比赛开始时间的间隔，可以为正或负

        # 发起查询
        line = CompetitionTime.objects.filter(studentnumber=student_number)
        for i in line:  # 对于每一条报名记录，查询有没有和当前比赛一致的
            if i.competition_name == event.competition_name and i.competition_turn == event.competition_turn and i.cubeevent == event.cubeevent:
                signed = 1
                break

        trans_list_element.append(event.competition_name)
        trans_list_element.append(event.competition_turn)
        trans_list_element.append(start_time.strftime('%Y-%m-%d %H:%M'))
        trans_list_element.append(event.cubeevent)
        if real_duration < 0:
            if signed == 1:
                trans_list_element.append('已报名')
                trans_list_element.append('取消报名')
                trans_list_element.append(row*10+2)  # 这个可以给不同位置的按钮上不同的id，以区分同时出现的两个相同类型的按钮
            else:
                trans_list_element.append('未报名')
                trans_list_element.append('报名')
                trans_list_element.append(row * 10 + 1)

        elif real_duration<lasting_time:
            trans_list_element.append('进行中')
            if signed == 0:
                trans_list_element.append('报名')
                trans_list_element.append(row * 10 + 3)
            else:
                trans_list_element.append('参加比赛')
                trans_list_element.append(row * 10 + 4)
            trans_list_element.append(None)

        else:
            trans_list_element.append('已结束')
            trans_list_element.append(None)

        trans_list.append(trans_list_element)

        row+=1

    return render(request, 'competition.html', {'competitions': trans_list})


def competition_register(request):
    student_number = request.session['student_number']
    competition_name = request.POST.get('a')
    competition_turn = request.POST.get('b')
    cube_event = request.POST.get('c')
    # 发起查询
    eventlist = CompetitionTime.objects.filter(studentnumber=student_number,competition_name=competition_name,competition_turn=competition_turn,cubeevent=cube_event)
    for line in eventlist:  # 报名信息已经存在，刷新
        return redirect('/competition')
    CompetitionTime.objects.create(competition_name=competition_name,competition_turn=competition_turn,
                                    cubeevent=cube_event,studentnumber=student_number,
                                    time1=None,time2=None,time3=None,time4=None,time5=None,single=None,average=None)
    return redirect('/competition')

def competition_cancel(request):
    student_number = request.session['student_number']
    competition_name = request.POST.get('a')
    competition_turn = request.POST.get('b')
    cube_event = request.POST.get('c')
    # 发起查询
    eventlist = CompetitionTime.objects.filter(studentnumber=student_number, competition_name=competition_name,
                                               competition_turn=competition_turn, cubeevent=cube_event).delete()
    return redirect('/competition')
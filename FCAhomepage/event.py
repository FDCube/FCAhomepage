from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from database.models import Person,Competition,CompetitionTime
import datetime
import decimal
from FCAhomepage.core.utils import single,average,sec_to_minute

def event(request):
    student_number = request.session['student_number']
    eventlist = Competition.objects.all()
    #eventlist = list(eventlist)  # 每个项目一个列表
    signed = 0
    event_name = []  # 传入前端的正在进行的项目列表，这里默认同一时间不会举办两场比赛
    # 传入比赛和项目名称
    for event in eventlist:
        start_time = event.competition_time
        start_time = start_time.replace(tzinfo=None)  # 转换为无时区时间，这样才能相减
        lasting_time = event.duration  # 获取比赛持续时间，分钟为单位
        now_time = datetime.datetime.now()
        real_duration = ((now_time - start_time).days * 86400 + (
                    now_time - start_time).seconds) / 60  # 现在时间与比赛开始时间的间隔，可以为正或负
        # 发起查询
        line = CompetitionTime.objects.filter(studentnumber=student_number)
        for i in line:  # 对于每一条报名记录，查询有没有和当前比赛一致的
            if i.competition_name == event.competition_name and i.competition_turn == event.competition_turn and i.cubeevent == event.cubeevent:
                if real_duration > 0 and real_duration < lasting_time :  # 比赛正在进行中并且已经报名
                    competition_name = event.competition_name  # 不出意外不会变
                    round = event.competition_turn  # 不出意外不会变
                    event_name.append(event.cubeevent)
                    event_now = i.cubeevent  # 如果不加指定（没有主动选中项目），默认选中第一个项目
                    signed = 1

        if signed == 0:  # 没有报名任何正在进行的比赛
            competition_name = ' '  # 一个空格

    event_now = request.session['event']  # 如果session里有event，更改event_now
    if request.POST:  # 如果接受了下拉框选择或线上赛页面直接进入的post，改变event_now
        event_now = request.POST.get('a')
    request.session['event'] = event_now

    # 传入已经计时的成绩
    if signed == 1:
        scores = []  # 传入前端的成绩，[(),(),()...]
        line = CompetitionTime.objects.filter(studentnumber=student_number,competition_name=competition_name,
                                              competition_turn=round,cubeevent=event_now)
        for i in line:  # 应该只有一条记录
            times=[i.time1, i.time2, i.time3, i.time4, i.time5 ]  # 时间数组，处理用
        #print(times)
        times = list(filter(lambda a: a != None, times))  # 删掉所有的None
        if len(times) < 5:
            times.append('')  # 为了生成开始按钮

        for i1 in range(0,len(times)) :
            scores.append((i1+1, times[i1]))

    # 传入当前比赛各个项目的排行
    all_events = []
    lines = Competition.objects.filter(competition_name=competition_name,competition_turn=round)
    for line in lines:  # 对于每一个项目
        signed = 0
        my_record= CompetitionTime.objects.filter(studentnumber=student_number,competition_name=competition_name,
                                              competition_turn=round,cubeevent=line.cubeevent)  # 在成绩表中找到属于自己的一行
        for i in my_record:
            signed=1
            my_timelist=[i.time1,i.time2,i.time3,i.time4,i.time5,]
        if signed:
            my_timelist = list(filter(lambda a: a != None, my_timelist))  # 删掉所有的None
            if len(my_timelist) <5:  # 没有满5次，默认不生成单次和平均成绩
                sin = ' '
                avg = ' '
                sin_rank = '-'
                avg_rank = '-'
            else:  # 满5次了，需要生成
                sin_rank = 1
                avg_rank = 1
                for i in my_record:
                    sin = i.single
                    avg = i.average
                records = CompetitionTime.objects.filter(competition_name=competition_name,
                                              competition_turn=round,cubeevent=line.cubeevent)  # 别人在这个项目中的成绩
                for record in records:
                    if record.single != None:  # 别人有成绩，才能比较
                        if record.single < sin:sin_rank+=1
                        if record.average < avg:avg_rank+=1
                sin = sec_to_minute(sin)  # 转换成分秒显示
                avg = sec_to_minute(avg)
                if str(sin) == '9999.99':sin = 'DNF'
                if str(avg) == '9999.99':avg = 'DNF'
            all_events.append({'name': line.cubeevent, 'single': sin, 'average': avg, 'sin_rank': sin_rank, 'avg_rank': avg_rank})
        else:  # 没有报名这个项目
            all_events.append(
                {'name': line.cubeevent, 'single': ' ', 'average': ' ', 'sin_rank': '-', 'avg_rank': '-'})

    '''
    all_events = [
        {'name': "三阶", 'single': "12.50", 'average': "13.66", 'sin_rank': "4", 'avg_rank': "3"},
        {'name': "二阶", 'single': "4.50", 'average': "5.66", 'sin_rank': "2", 'avg_rank': "2"},
        {'name': "四阶", 'single': "56.02", 'average': "1:01.22", 'sin_rank': "5", 'avg_rank': "5"},
        {'name': "五阶", 'single': "1:56.50", 'average': "2:00.00", 'sin_rank': "6", 'avg_rank': "3"},
    ]  # 全部项目
    #scores = [(1, "13.34+"),(2, "")]  # 当前项目成绩
    '''

    return render(request, 'event.html', {'competition_name': competition_name, 'event_name': event_name,'selected':event_now, 'round': round,
                                          'all_events': all_events, 'scores': scores, })

def event_start(request):
    if request.method == "POST" and request.POST:
        competition_ = request.POST.get('competition_name')
        event_ = request.POST.get('event')
        round_ = request.POST.get('round')
        num_ = request.POST.get('num')
        # 存在session里
        request.session['competition_name'] = competition_
        #request.session['event'] = event_  # 前面event函数已经存过了
        request.session['round'] = round_
        request.session['num'] = num_

        if event_ is not None and round_ is not None and num_ is not None:
            round_ = int(round_)
            num_ = int(num_)
            # 获取对应打乱
            line = Competition.objects.filter(competition_name=competition_,competition_turn=round_,cubeevent=event_)
            for i in line:
                scramblelist = [i.scramble1,i.scramble2,i.scramble3,i.scramble4,i.scramble5,i.scramble_extra1,i.scramble_extra2]

        return render(request, 'compete_timer.html')
    return redirect('/competition')

def event_submit(request):
    student_number = request.session['student_number']
    competition_name = request.session['competition_name']
    round = request.session['round']
    event = request.session['event']
    num = request.session['num']
    line = CompetitionTime.objects.filter(studentnumber=student_number, competition_name=competition_name,
                                          competition_turn=round, cubeevent=event)
    if request.method == "POST" and request.POST:
        score = request.POST.get('a')

    num = int(num)
    if num == 1:
        line.update(time1=score)
    elif num == 2:
        line.update(time2=score)
    elif num == 3:
        line.update(time3=score)
    elif num == 4:
        line.update(time4=score)
    elif num == 5:
        line.update(time5=score)
        for i in line:
            my_timelist = [i.time1,i.time2,i.time3,i.time4,i.time5]
        timelist1=my_timelist.copy();timelist2=my_timelist.copy()  # 因为求平均和单次的函数要改变数组，所以传入copy后的数组
        line.update(single=decimal.Decimal(single(timelist1)),average=decimal.Decimal(average(timelist2)))


    #return HttpResponse(event+num+score)
    return redirect('/event')
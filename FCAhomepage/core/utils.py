import decimal,math

def minute_to_sec(time1):  # 把成绩的分钟转换成秒，才能存进数据库里
    if ':' not in time1: return decimal.Decimal(time1)
    list = time1.split(':', 1)
    time2 = 60*decimal.Decimal(list[0]) + decimal.Decimal(list[1])
    return time2

def sec_to_minute(time2):  # 从校记录数据库取出的是秒，需要转换成分钟显示。
    dec = decimal.Decimal(time2)
    if dec<60: return time2
    min = math.floor(dec/60)
    sec = dec - min*60
    if sec < 10:
        return str(min) + ':0' + str(sec)
    else:
        return str(min)+':'+str(sec)

def average(timelist):  # 给5个时间（str形式，包含 +和DNF），算出AVG（decimal形式，DNF为9999.99）
    Dcount = 0
    for i in range(0,5):
        if timelist[i] == 'DNF':
            timelist[i] = decimal.Decimal('9999.99')
            Dcount += 1
        elif '+' in timelist[i]:  # 包含+
            list = timelist[i].split(' ', 1)
            timelist[i] = minute_to_sec(list[0])
        else:
            timelist[i] = minute_to_sec(timelist[i])
    if Dcount > 1:return decimal.Decimal('9999.99')
    #print(timelist)
    result = (sum(timelist) - min(timelist) - max(timelist)) / 3
    return round(result,2)

def single(timelist):  # 给0-5个时间（str形式，包含 +和DNF），算出single（decimal形式）
    if len(timelist) == 0:return ' '  # 一个空格
    for i in range(0,len(timelist)):
        if timelist[i] == 'DNF':
            timelist[i] = decimal.Decimal('9999.99')
        elif '+' in timelist[i]:  # 包含+
            list = timelist[i].split(' ', 1)
            timelist[i] = minute_to_sec(list[0])
        else:
            timelist[i] = minute_to_sec(timelist[i])
    return min(timelist)

#a=['1:09.45', 'DNF','DNF','10:12.34 +','55.55']
#print(single(a))
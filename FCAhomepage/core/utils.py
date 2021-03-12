import decimal,math

def minute_to_sec(time1):  # 把成绩的分钟转换成秒，才能存进数据库里
    if ':' not in time1: return time1
    list = time1.split(':', 1)
    time2 = 60*decimal.Decimal(list[0]) + decimal.Decimal(list[1])
    return time2

def sec_to_minute(time2):  # 从数据库取出的是秒，需要转换成分钟显示。
    dec = decimal.Decimal(time2)
    if dec<60: return time2
    min = math.floor(dec/60)
    sec = dec - min*60
    if sec < 10:
        return str(min) + ':0' + str(sec)
    else:
        return str(min)+':'+str(sec)


#print(sec_to_minute('100.54'))
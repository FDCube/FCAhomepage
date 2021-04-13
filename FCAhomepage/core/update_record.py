from FCAhomepage.core.search_wca import get_competitor_by_wca_id
from FCAhomepage.core.utils import minute_to_sec,sec_to_minute
import decimal
import pymysql  # 这里我还是决定用pymysql，和网页无关，手动更新校记录。每隔一段时间执行此程序即可根据所有在校同学的id更新校记录

connection = pymysql.connect(host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',
                       port=3306,
                       user='lab_1693260529',
                       passwd='e939cbe1ea4a_#@Aa',
                       db='polardb_mysql_zl2048')
cursor = connection.cursor()
EventList = ['三阶','二阶','四阶','五阶','六阶', '七阶','单手','三盲','四盲','金字塔','斜转','SQ1','魔表','最少步']

'''测试
for event in EventList:
    print(event)
    sql="SELECT name_single " \
            "FROM record " \
            "WHERE CubeEvent=%s "
    cursor.execute(sql,event)
    for i in cursor:
        print(i[0])
'''

def update_record(competitor):  # 对于一个人，在校记录中更新他的位置
    for event in EventList:  # 对于每个wca项目
        if ' '+event in competitor.records.keys():  # 如果他在该项目中有成绩
            print(event)
            single = minute_to_sec(competitor.records[' '+event].single)
            single = decimal.Decimal(single)
            average = minute_to_sec(competitor.records[' ' + event].average)
            if average != 'DNF': average = decimal.Decimal(average)
            # 单次，发起查询，看看是否比校记录高
            sql = "SELECT time_single " \
                  "FROM record " \
                  "WHERE CubeEvent=%s "
            cursor.execute(sql, event)
            for i in cursor:
                record_single = i[0]
            if single <= record_single:  # 比校记录快
                sql = "UPDATE record " \
                      "SET time_single=%s, name_single=%s " \
                      "WHERE CubeEvent=%s"
                cursor.execute(sql, [single, competitor.name,event])
                cursor.execute("""drop table if exists test""")  # 不进行这步插不进去

            if average == 'DNF':  #
                continue
            # 平均，和单次一样处理
            sql = "SELECT time_average " \
                  "FROM record " \
                  "WHERE CubeEvent=%s "
            cursor.execute(sql, event)
            for i in cursor:
                record_average = i[0]
            if average <= record_average:  # 比校记录快
                sql = "UPDATE record " \
                      "SET time_average=%s, name_average=%s " \
                      "WHERE CubeEvent=%s"
                cursor.execute(sql, [average, competitor.name, event])
                cursor.execute("""drop table if exists test""")  # 不进行这步插不进去



if __name__ == '__main__':
    competitor = get_competitor_by_wca_id("2013MAZA01")
    #single = competitor.records[' 四阶'].single
    #if ':' in single: print(minute_to_sec(single))
    update_record(competitor)



"""
爬取粗饼的成绩

html
选手主页-结构
<body>
    <div class="wrapper">
        <div class="content container">
            <div class="page-wrapper">
                <div class="page-content">
                    <div class="row page-row">
                        <div class="col-lg-12 results-person" data-person-id="{{WCA ID}}">
                            <h1 class="text-center">{{英语名}} ({{中文名}})</h1>
                            <div class="panel panel-info person-detail">
                                <div class="panel-body">
                                    <div class="row">
                                        <div class="col-md-4 col-sm-6 col-xs-12 mt-10">             /*这部分包括：姓名、地区、参赛次数、ID、性别、经历*/
                                            <span class="info-title">{{标题}}:</span>
                                            <span class="info-value">{{内容}}</span>
                                        <div> ......
                        <div class="table-responsive" id="yw0">
                            <table class="table table-bordered table-condensed table-hover table-boxed">
                                <tr>                                                                /*第一行是表头*/
                                <tr>  class="odd" || "even"                                         /*每个项目的成绩、排名*/
                                    <td><a href="#333"><i title="三阶"></i> 三阶</a></td>                /*项目*/
                                    <td>6994</td>                                                       /*地区排名*/
                                    <td>17412</td>                                                      /*洲排名*/
                                    <td>42105</td>                                                      /*世界排名*/
                                    <td><a>17.48</a></td>                                               /*单次*/
                                    <td><a>21.18</a></td>                                               /*平均*/
                                    <td>42669</td>                                                      /*世界排名*/
                                    <td>17723</td>                                                      /*洲排名*/
                                    <td>7072</td>                                                       /*地区排名*/
                                    <td></td>                                                           /*金*/
                                    <td></td>                                                           /*银*/
                                    <td></td>                                                           /*铜*/
                                    <td>10/10</td>                                                      /*复原/尝试*/
                                <tr> ......

"""

import requests
import re
import bs4
from typing import Optional, List, Dict

url_cubing_china = "http://cubingchina.com"
RE_name = re.compile(r"([\w\n ]+) \((.+)\)")


class Competitor:
    """选手"""
    MALE = 0
    FEMALE = 1

    def __init__(self, name, name_en):
        self.name = name
        self.name_en = name_en
        self.id = ""
        self.gender = 0
        self.region = ""
        self.comp_count = 0
        self.career = ""
        self.records = {}

    def set_gender(self, gender):
        if gender == '男':
            self.gender = self.MALE
        elif gender == '女':
            self.gender = self.FEMALE

    def __str__(self):
        ret = "姓名: {} ({}); ID: {}; 地区: {}; 参赛次数: {};".format(self.name, self.name_en,
                                                              self.id, self.region, self.comp_count)
        for record in self.records.values():
            ret += "\n" + str(record)
        return ret


class CubeEvent:
    """项目"""

    def __init__(self, name, single, average, times):
        self.name = name
        self.single = single if single else "DNF"
        self.average = average if average else "DNF"
        self.times = times

    def __str__(self):
        return f"{self.name:<10}{self.single:<10}{self.average:<10}{self.times}"


def get_html_by_url(url: str) -> str:
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = requests.get(url, headers=headers, timeout=30)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        return req.text
    except:
        print("拒绝访问")
        return ""


def get_competitor_by_wca_id(wca_id: str) -> Optional[Competitor]:
    url = url_cubing_china + "/results/person/" + wca_id.upper()
    print(url)
    str_html = get_html_by_url(url)

    soup = bs4.BeautifulSoup(str_html, "html.parser")

    # 中英文姓名
    h1_name = soup.find("h1", attrs={"class": "text-center"})
    if h1_name:
        res = RE_name.match(h1_name.text)
        if res:
            competitor = Competitor(res.group(2), res.group(1))

        else:
            competitor = Competitor('江晓晖', h1_name.text)
            print("姓名解析错误")
            #return None
    else:
        print("选手不存在")
        return None
    print(competitor.name)
    # 基本信息
    span_title = soup.find_all("span", attrs={"class": "info-title"})
    span_value = soup.find_all("span", attrs={"class": "info-value"})
    for title, value in zip(span_title, span_value):
        # print(title.text, value.text.strip())
        if title.text == "地区:":
            competitor.region = value.text.strip()
        elif title.text == "参赛次数:":
            competitor.comp_count = int(value.text.strip())
        elif title.text == "性别:":
            competitor.set_gender(value.text.strip())
        elif title.text == "参赛经历:":
            competitor.career = value.text.strip()
        elif title.text == "WCA ID:":
            competitor.id = value.text.strip()
        else:
            pass
    # 项目成绩
    table_score = soup.find("table")
    tr_event = table_score.find_all("tr")
    for tr in tr_event[1:]:
        td_s = tr.find_all("td")
        event = CubeEvent(td_s[0].text, td_s[4].text, td_s[5].text, td_s[12].text)
        #print(event)
        #print(td_s[0].text)
        competitor.records[td_s[0].text] = event

    print(competitor)
    return competitor



if __name__ == '__main__':
    get_competitor_by_wca_id("2018DONG13")
    get_competitor_by_wca_id("2013MAZA01")
    get_competitor_by_wca_id("2018JIAN42")

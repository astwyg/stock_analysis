import requests, io
from bs4 import BeautifulSoup
from simplejson.errors import JSONDecodeError

def download_page(d):
    url = "http://chinext.zqrb.cn/html/{}/news-{}-{}.html".format(d["create_time"],d["classId"],d["afficheId"])
    r = requests.get(url)
    r.encoding = 'gbk'
    page =  BeautifulSoup(r.text)
    title = d["title"]
    with io.open("..\\..\\data\\csrc\\market_chuangye_2year\\"+title+".txt", "w", encoding="utf-8") as fw:
        content = page.select("div#content")
        fw.write("\n".join([c.text for c in content]))

def get_links(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    try:
        data = r.json()
    except JSONDecodeError:
        return
    for d in data:
        if "审核结果" in d["title"]:
            download_page(d)


def get_all_pages():
    for year in range(2019, 2016, -1):
        for month in range(12, 0, -1):
            if year == 2019 and month > 7:
                continue
            get_links("http://chinext.zqrb.cn/json/classdata/class_197/{}/{}.js".format(year, str(month).zfill(2)))

if __name__=="__main__":
    get_all_pages()
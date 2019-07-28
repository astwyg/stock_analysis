import requests, io
from bs4 import BeautifulSoup
from simplejson.errors import JSONDecodeError

def download_page(d):
    url = "http://kcb.zqrb.cn/html{}news-{}-{}.html".format(d["afficheAddress"],d["classId"],d["afficheId"])
    r = requests.get(url)
    r.encoding = 'gbk'
    page =  BeautifulSoup(r.text)
    title = d["title"]
    with io.open("..\\..\\data\\csrc\\market_kechuang_all\\"+title+".txt", "w", encoding="utf-8") as fw:
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
        if "结果公告" in d["title"]:
            download_page(d)


def get_all_pages():
    for year in range(2019, 2016, -1):
        for month in range(12, 0, -1):
            if year == 2019 and month > 7:
                continue
            get_links("http://kcb.zqrb.cn/json/classdata/class_173/{}/{}.js".format(year, str(month).zfill(2)))

if __name__=="__main__":
    get_all_pages()
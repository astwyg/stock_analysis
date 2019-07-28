import requests, io
from bs4 import BeautifulSoup

def download_page(a):
    url = "http://ipo.qianzhan.com"+a.attrs["href"].split("../")[-1]
    r = requests.get(url)
    r.encoding = 'utf-8'
    page =  BeautifulSoup(r.text)
    title = a.text.replace("\r","").replace("\n","").replace(" ","")
    with io.open("..\\..\\data\\csrc\\market_A_2year\\"+title+".txt", "w", encoding="utf-8") as fw:
        content = page.select("pre")
        fw.write(content[0].text)

def get_links(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    page = BeautifulSoup(r.text)
    links = page.select("div.right ul li")
    for link in links:
        try:
            a = link.select("a")[0]
            if "审核结果" in a.text:
                download_page(a)
            print(a.text)
        except AttributeError:
            continue

def get_all_pages():
    for i in range(1, 36):
        get_links("http://ipo.qianzhan.com/zjh/gglist-{}.html".format(i))

if __name__=="__main__":
    get_all_pages()
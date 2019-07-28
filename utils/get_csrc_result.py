import requests, io
from bs4 import BeautifulSoup

def download_page(link):
    url = "http://www.csrc.gov.cn/pub/"+link.attrs["href"].split("../")[-1]
    r = requests.get(url)
    r.encoding = 'utf-8'
    page =  BeautifulSoup(r.text)
    with io.open("..\\data\\csrc\\"+link.text+".txt", "w", encoding="utf-8") as fw:
        content = page.find_all("div", class_="contentss")[0]
        content = content.find_all("p")
        fw.write("\n".join([c.text for c in content]))

def get_links(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    page0 = BeautifulSoup(r.text)
    contents = page0.find_all("div", class_="fl_list")
    contents = contents[0].contents[1].contents
    for c in contents:
        try:
            link = c.find_all("a")[0]
            if "审核结果" in link.text:
                download_page(link)
            print(link.text)
        except AttributeError:
            continue

def get_all_pages():
    get_links("http://www.csrc.gov.cn/pub/newsite/zxgx/jigbsdt/index.html")
    for i in range(1, 25):
        get_links("http://www.csrc.gov.cn/pub/newsite/zxgx/jigbsdt/index_{}.html".format(i))

if __name__=="__main__":
    get_all_pages()
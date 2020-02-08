import time
import tushare as ts
import requests
from bs4 import BeautifulSoup

def get_all_stock_num():
    ts.set_token('63fa7782075b5409355fef5dc288adc9bc7250fd5fb1bade38eb37bc')
    pro = ts.pro_api()
    data = pro.stock_basic()
    all_stock = data['ts_code'].tolist()
    return all_stock

def download_annual_report(stock_num):
    page1 = requests.get("http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/{}.phtml?ftype=ndbg".format(stock_num))
    page1.encoding = "gb2312"
    page1 = BeautifulSoup(page1.text)
    if "英文" in page1.find_all("div", class_="datelist")[0].contents[0].contents[1].text:
        next_url = page1.find_all("div", class_="datelist")[0].contents[0].contents[4]["href"] # bypass <br> and text.
    else:
        next_url = page1.find_all("div", class_="datelist")[0].contents[0].contents[1]["href"]
    page2 = requests.get("http://vip.stock.finance.sina.com.cn/"+next_url)
    page2.encoding = "gb2312"
    page2 = BeautifulSoup(page2.text)
    content = page2.find_all("div", class_="graybgH2")[0].contents[1]
    name = page2.find_all("th",style="text-align:center")[0].contents[0].replace("\t","")
    name = name.replace("*","").replace("?","")
    with open("..\\data\\annual_report_2018_txt_new\\{}.txt".format(stock_num+"_"+name),"w", encoding='utf-8') as f:
        f.write(str(content))



if __name__ == "__main__":
    all_stock = get_all_stock_num()
    for stock in all_stock[1170:]:  # 改起点位置
        try:
            download_annual_report(stock.split(".")[0])
        except IndexError:
            print("{}没找到".format(stock))
        time.sleep(12)
        print("downloaded "+stock)
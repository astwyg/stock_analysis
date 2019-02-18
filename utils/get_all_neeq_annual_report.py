import requests, re, json, time

def get_annual_report(stock_num):
    print(stock_num)
    page = requests.post("http://www.neeq.com.cn/disclosureInfoController/infoResult.do?callback=jQuery18303350037129771044_1550474363159",
                         data={
                             "disclosureType":"1",
                             "page":"0",
                             "companyCd":stock_num,
                             "isNewThree":"1",
                             "startTime":"",
                             "endTime":"",
                             "keyword":"关键字",
                             "xxfcbj":""
                         })
    text = re.findall(r"[(](.*?)[)]", page.text)[0]
    try:
        title = json.loads(text)[0]["listInfo"]["content"][0]["disclosureTitle"]
    except json.decoder.JSONDecodeError:
        with open("..\\data\\neeq_annual_report_2018H1\\{}_failed.txt".format(stock_num), "w") as f:
            f.write(stock_num)
        return
    title = title.replace(":","_").replace("*","_")
    file_path = json.loads(text)[0]["listInfo"]["content"][0]["destFilePath"]
    pdf_file = requests.get("http://www.neeq.com.cn" + file_path, headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",
    }, stream=True)
    with open("..\\data\\neeq_annual_report_2018H1\\{}.pdf".format(title),"wb") as f:
        for chunk in pdf_file.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    # time.sleep(5)

def get_all_stock():
    page0 = requests.get("http://www.neeq.com.cn/nqxxController/nqxx.do?callback=jQuery1830483533568956642_1550473485680&page=0&typejb=T&xxzqdm=&xxzrlx=&xxhyzl=&xxssdq=&sortfield=xxzqdm&sorttype=asc&dicXxzbqs=&xxfcbj=&_=1550473497322")
    text = re.findall(r"[(](.*?)[)]", page0.text)[0]
    totalPages = json.loads(text)[0]["totalPages"]
    for page_num in range(totalPages):
        page = requests.get("http://www.neeq.com.cn/nqxxController/nqxx.do?callback=jQuery1830483533568956642_1550473485680&page={}&typejb=T&xxzqdm=&xxzrlx=&xxhyzl=&xxssdq=&sortfield=xxzqdm&sorttype=asc&dicXxzbqs=&xxfcbj=&_=1550473497322".format(page_num))
        text = re.findall(r"[(](.*?)[)]", page.text)[0]
        contents = json.loads(text)[0]["content"]
        for content in contents:
            get_annual_report(content["xxzqdm"])
        # time.sleep(5)

if __name__ == "__main__":
    get_all_stock()
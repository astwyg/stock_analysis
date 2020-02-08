import os

def find_keyword(keyword, path):
    for root, dirs, files in os.walk(path):
        for f in files:
            with open(os.path.join(path, f),"r", encoding="utf-8") as fp:
                content = fp.read()
                keyword_times = content.count(keyword)
                if keyword_times:
                    print("{}在{}中出现{}次".format(keyword,f,keyword_times))


if __name__ == "__main__":
    keyword = input("输入关键字:")
    find_keyword(keyword, path = "..\\data\\annual_report_2018_txt_new")
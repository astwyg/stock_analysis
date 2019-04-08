import os
import pdfplumber

path = "..\\data\\neeq_annual_report_2018H1"

def find_keyword(keyword):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith("pdf"):
                with pdfplumber.open(os.path.join(path, f)) as pdf:
                    keyword_cnt = 0
                    for page in pdf.pages:
                        keyword_cnt = keyword_cnt + page.extract_text().count(keyword)
                    if keyword_cnt:
                        print("{}在{}中出现{}次".format(keyword, f, keyword_cnt))

if __name__ == "__main__":
    keyword = input("输入关键字:")
    find_keyword(keyword)
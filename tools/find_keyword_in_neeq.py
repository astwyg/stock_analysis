from tools.fnd_keyword_in_annual_report import find_keyword

if __name__ == "__main__":
    keyword = input("输入关键字:")
    find_keyword(keyword, path="..\\data\\neeq_annual_report_2018H1_txt")
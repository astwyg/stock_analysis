import os
import baostock as bs
import pandas as pd


path = "..\\data\\annual_report_2018_txt"

keywords = ["软件","国产化"]

def find_keyword(keyword):
    for root, dirs, files in os.walk(path):
        for f in files:
            with open(os.path.join(path, f),"r", encoding="utf-8") as fp:
                content = fp.read()
                keyword_times = content.count(keyword)
                if keyword_times:
                    print("{}在{}中出现{}次".format(keyword,f,keyword_times))


def find_keywords():
    with open(os.path.join("..\\data\\industry_insight","_".join(keywords)+".csv"),"w") as result_f:
        result_f.write("股票代码, 公司名称, {}".format("+".join(keywords))+"\n")
        for root, dirs, files in os.walk(path):
            for f in files:
                with open(os.path.join(path, f), "r", encoding="utf-8") as fp:
                    content = fp.read()
                    keyword_cnt = []
                    keyword_flag = False
                    for keyword in keywords:
                        keyword_cnt.append(str(content.count(keyword)))
                        if not content.count(keyword):
                            keyword_flag = False
                            break
                        else:
                            keyword_flag = True

                    if keyword_flag:
                        result_f.write("{},{},{}\n".format(
                            "'"+f.split("_")[0],
                            f.split("_")[1].split("20")[0],
                            "+".join(keyword_cnt)
                        ))

def get_full_stock_number(stock):
    tmp = stock[-6:]
    if tmp[0] in ["0","3","2"]:
        tmp = "sz."+tmp
    else:
        tmp = "sh."+tmp
    return tmp

def stock_analysis():
    bs.login()
    with open(os.path.join("..\\data\\industry_insight", "_".join(keywords) + ".csv"), "r") as source_f:
        with open(os.path.join("..\\data\\industry_insight", "_".join(keywords) + "_result.csv"), "w") as result_f:
            first_line = True
            for source_line in source_f:
                if first_line:
                    result_f.write(source_line[:-2]+",peTTM(滚动市盈率),psTTM(滚动市销率),pcfNcfTTM(滚动市现率),pbMRQ(市净率),2017MBRevenue, 2017netProfit, 2018MBRevenue, 2018netProfit\n")
                    first_line = False
                    continue
                stock_number = get_full_stock_number(source_line.split(",")[0])

                # source info
                result_f.write(source_line.replace("\n",""))

                # pe and ps
                rs = bs.query_history_k_data_plus(stock_number,
                                                  "date,code,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                                                  start_date='2019-04-04', end_date='2019-04-04',
                                                  frequency="d", adjustflag="3")
                result_list = []
                while (rs.error_code == '0') & rs.next():
                    result_list.append(rs.get_row_data())
                result = pd.DataFrame(result_list, columns=rs.fields)
                result_f.write("," + ",".join(result.loc[0][-4:]))

                # 2018 and 2019 finance
                try:
                    rs_profit = bs.query_profit_data(code=stock_number, year=2017, quarter=4)
                    profit_list = []
                    while (rs_profit.error_code == '0') & rs_profit.next():
                        profit_list.append(rs_profit.get_row_data())
                    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
                    result_f.write("," + str(result_profit.iloc[0]["MBRevenue"])+","+str(result_profit.iloc[0]["netProfit"]))

                    rs_profit = bs.query_profit_data(code=stock_number, year=2018, quarter=4)
                    profit_list = []
                    while (rs_profit.error_code == '0') & rs_profit.next():
                        profit_list.append(rs_profit.get_row_data())
                    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
                    result_f.write("," + str(result_profit.iloc[0]["MBRevenue"]) + "," + str(result_profit.iloc[0]["netProfit"]))
                except IndexError:  # 有些18年报还没出
                    pass

                result_f.write("\n")
                # break # debuging

    bs.logout()

if __name__ == "__main__":
    # find_keywords()
    stock_analysis()
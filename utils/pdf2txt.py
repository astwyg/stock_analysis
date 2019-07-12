import os, codecs
import pdfplumber

pdf_path = "..\\data\\neeq_annual_report_2018H1"
txt_path = "..\\data\\neeq_annual_report_2018H1_txt"

def convert():
    cnt = 0
    for root, dirs, files in os.walk(pdf_path):
        for f in files:
            cnt = cnt + 1
            print("{}/{}".format(cnt, len(files)))
            if f.endswith("pdf"):
                with pdfplumber.open(os.path.join(pdf_path, f)) as pdf:
                    txt_filename = f.split(".")[-2] + ".txt"
                    with codecs.open(os.path.join(txt_path, txt_filename), "w", encoding="utf-8") as new_f:
                        for page in pdf.pages:
                            new_f.write(page.extract_text())

if __name__ == "__main__":
    convert()
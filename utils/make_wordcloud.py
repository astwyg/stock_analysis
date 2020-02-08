import os
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import matplotlib.pyplot as plt


def get_content(path):
    all_content = ""
    for root, dirs, files in os.walk(path):
        for f in files:
            with open(os.path.join(path, f),"r", encoding="utf-8") as fp:
                content = fp.read()
                all_content = all_content + content
    return all_content

def make_wordcloud(path):
    text = get_content(path)
    cut_text = ' '.join(jieba.cut(text))
    stopwords = set()
    stopwords.update([])


    wc = WordCloud(
        font_path='c:\windows\Fonts\simhei.ttf',
        background_color = 'white',
        scale = 15,
        stopwords=stopwords,
    ).generate(cut_text)

    process_word = WordCloud.process_text(wc, cut_text)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    # print(sort[:50])  # 输出前词频最高的前50个, 调试停止词用.
    for i in sort[:50]:
        print(i)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    wc.to_file("pjl_cloud1.jpg")

if __name__=="__main__":
    make_wordcloud("..\\data\\csrc\\market_kechuang_all")
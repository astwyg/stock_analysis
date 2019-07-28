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
    stopwords.update(["发行人", "是否", "发行人 代表", "保荐 代表人", "因此", "我们", "一个", "如果",
                      '它们', '具有', '人们', '可以', '这个', '这种', '不能', '因为',
                      '或者', '没有', '这些', '一种', '非常', '可能', '他们', '而且',
                      '所有', '也许', '就是', '认为', '正如', '必须', '确定', '所以',
                      '任何', '发生', '甚至', '能够', '过去', '对于', '知道', '这是',
                      '现在', '不同', '并且', '似乎', '那样', '其他', '什么', '不是',
                        '那么', '一点', '已经', '之间', '如何', '仍然'])


    wc = WordCloud(
        font_path='c:\windows\Fonts\simhei.ttf',
        background_color = 'white',
        scale = 15,
        stopwords=stopwords,
    ).generate(cut_text)

    process_word = WordCloud.process_text(wc, cut_text)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    print(sort[:50])  # 输出前词频最高的前50个, 调试停止词用.

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    wc.to_file("pjl_cloud2.jpg")

if __name__=="__main__":
    make_wordcloud("..\\data\\csrc\\market_A_2year")
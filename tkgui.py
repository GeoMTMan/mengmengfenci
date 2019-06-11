from tkinter import *
import codecs
import math


'''贝叶斯分词需要调用的lambda表达式和方法solve'''
#############################################################################
d = {}
log = lambda x: float('-inf') if not x else math.log(x)
    # 匿名函数
prob = lambda x: d[x] if x in d else 0 if len(x) > 1 else 1

#贝叶斯方法词典的导入
def init(filename='SogouLabDic.dic'):
    d['_N_'] = 0.0
    with open(filename, 'r',encoding='gb18030') as handle:
        for line in handle:
            # print(line)
            word, freq = line.split('\t')[0:2]  # 取list的前2个元素,词和相应的词数
            d['_N_'] += int(freq)+1             # 此表的词频总和,每个词数都加1
            try:
                # print('utf')
                d[word.decode('utf-8')] = int(freq)+1 # 词数加1
            except:
                # print('gbk')
                try:
                    d[word] = int(freq)+1            # 词数加1
                except:
                    print(word)
                    break
#贝叶斯方法的主要计算过程
def solve(s):
    length = len(s)
    p = [0 for i in range(length + 1)]  # 1,2,...,l位置为0
    t = [0 for i in range(length)]
    # 如'大床房多少钱'，当前位置到末尾分别为1,2,...l长度的词，t[i]保留从当前位置向前划分的最佳长度，比如从'大'开始，
    # 大床最佳，或大床房最佳，取决词库
    for i in range(length - 1, -1, -1):  # start,stop，step
        # prob(s[i:i+k])/d['_t_']为词表词频度
        p[i], t[i] = max((prob(s[i:i + k]) / d['_N_'] + p[i + k], k)
                         # prob(s[i:i+k])/d['_N_']  + p[i+k]表示最大化已划分句子得分的过程，当前划分部分的字典频率+剩余部分的得分（已计算）
                         for k in range(1, length - i + 1))
        # 在一个二元组列表里返回第一个元素最大的二元组,
        # print(p[i], t[i])
    dis = 0
    while dis < length:  # dis=0,不断向前遍历分割词汇
        yield s[dis:dis + t[dis]]
        dis += t[dis]

#############################################################################



'''GUI类'''
class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
    '''GUI界面设计部分'''
    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("分词器")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="待处理文本")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="分词结果")
        self.result_data_label.grid(row=0, column=12)
        #文本框
        self.init_data_Text = Text(self.init_window_name, width=70, height=49)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        #按钮
        self.ZMM_button = Button(self.init_window_name, text="正向最大匹配", bg="lightblue", width=10,
                                 command=self.ZMM)  # 调用内部方法  加()为直接调用
        self.ZMM_button.grid(row=1, column=11)
        self.ZMM_button = Button(self.init_window_name, text="逆向最大匹配", bg="lightblue", width=10,
                                 command=self.NMM)  # 调用内部方法  加()为直接调用
        self.ZMM_button.grid(row=5, column=11)
        self.ZMM_button = Button(self.init_window_name, text="朴素贝叶斯", bg="lightblue", width=10,
                                 command=self.BayesWS)  # 调用内部方法  加()为直接调用
        self.ZMM_button.grid(row=9, column=11)

    '''正向最大匹配法'''

    #############################################################################
    def ZMM(self):
        # 获得分词字典，存储为字典形式
        f1 = codecs.open('D:\pycode\MaxMatch\SogouLabDicOnlyWord.txt', 'r', encoding='utf8')
        dic = {}
        while 1:
            line = f1.readline()
            if len(line) == 0:
                break
            term = line.strip()  # 去除字典两侧的换行符，避免最大分词长度出错
            dic[term] = 1
        f1.close()
        # 获得需要分词的文本，为字符串形式
        chars = self.init_data_Text.get(1.0, END).strip().replace("\n", "")
        print(chars)
        # 获得停用词典，存储为字典形式
        f3 = codecs.open('D:\pycode\MaxMatch\stop_words.txt', 'r', encoding='utf8')
        stoplist = {}
        while 1:
            line = f3.readline()
            if len(line) == 0:
                break
            term = line.strip()
            stoplist[term] = 1
        f3.close()
        # 正向匹配最大分词算法
        # 遍历分词词典，获得最大分词长度
        max_chars = 0
        for key in dic:
            if len(key) > max_chars:
                max_chars = len(key)
        print(max_chars)
        # 定义一个空列表来存储分词结果
        words = []
        n = 0
        while n < len(chars):
            matched = 0
            # range([start,] stop[, step])，根据start与stop指定的范围以及step设定的步长 step=-1表示去掉最后一位
            for i in range(max_chars, 0, -1):  # i等于max_chars到1
                s = chars[n: n + i]  # 截取文本字符串n到n+1位
                # 判断所截取字符串是否在分词词典和停用词词典内
                if s in dic:
                    if s in stoplist:  # 判断是否为停用词
                        words.append(s)
                        matched = 1
                        n = n + i
                        break
                    else:
                        words.append(s)
                        matched = 1
                        n = n + i
                        break
                if s in stoplist:
                    words.append(s)
                    matched = 1
                    n = n + i
                    break
            if not matched:  # 等于 if matched == 0
                words.append(chars[n])
                n = n + 1
        print('正向最大匹配分词结果：')
        print('/'.join('%s' % id for id in words))
        self.result_data_Text.delete(1.0, END)
        self.result_data_Text.insert(1.0, ('/'.join('%s' % id for id in words)))

    #############################################################################


    '''逆向最大匹配法'''

    #############################################################################
    def NMM(self):
        # 获得分词字典，存储为字典形式
        f1 = codecs.open('D:\pycode\MaxMatch\SogouLabDicOnlyWord.txt', 'r', encoding='utf8')
        dic = {}
        while 1:
            line = f1.readline()
            if len(line) == 0:
                break
            term = line.strip()  # 去除字典两侧的换行符，避免最大分词长度出错
            dic[term] = 1
        f1.close()
        # 获得需要分词的文本，为字符串形式
        chars = self.init_data_Text.get(1.0, END).strip().replace("\n", "")
        print(chars)
        # 获得停用词典，存储为字典形式
        f3 = codecs.open('D:\pycode\MaxMatch\stop_words.txt', 'r', encoding='utf8')
        stoplist = {}
        while 1:
            line = f3.readline()
            if len(line) == 0:
                break
            term = line.strip()
            stoplist[term] = 1
        f3.close()

        # 正向匹配最大分词算法
        # 遍历分词词典，获得最大分词长度
        max_chars = 0
        for key in dic:
            if len(key) > max_chars:
                max_chars = len(key)
        print(max_chars)
        # 定义一个空列表来存储分词结果
        words = []
        n = len(chars)  # 待分词文本的长度
        while n > 0:
            matched = 0
            # range([start,] stop[, step])，根据start与stop指定的范围以及step设定的步长 step=-1表示去掉最后一位
            for i in range(max_chars, 0, -1):  # i等于max_chars到1
                if n - i < 0:  # 若待分词文本长度小于最大字典词长，则终止循环
                    continue
                s = chars[n - i: n]  # 截取文本字符串n到n+1位
                # 判断所截取字符串是否在分词词典和停用词词典内
                if s in dic:
                    if s in stoplist:  # 判断是否为停用词
                        words.append(s)
                        matched = 1
                        n = n - i
                        break
                    else:
                        words.append(s)
                        matched = 1
                        n = n - i
                        break
                if s in stoplist:
                    words.append(s)
                    matched = 1
                    n = n - i
                    break
            if not matched:  # 等于 if matched == 0
                words.append(chars[n - 1: n])
                n = n - 1
            words.reverse()
        print('逆向最大匹配算法分词结果：')
        print('/'.join('%s' % id for id in words))
        self.result_data_Text.delete(1.0, END)
        self.result_data_Text.insert(1.0, ('/'.join('%s' % id for id in words)))

    #############################################################################

    '''贝叶斯分词法'''

    #############################################################################
    def BayesWS(self):
        init()
        st = self.init_data_Text.get(1.0, END).strip().replace("\n", "")
        lpp = list(solve(st))
        print('贝叶斯分词结果：')
        print('/'.join(list(solve(st))))
        self.result_data_Text.delete(1.0, END)
        self.result_data_Text.insert(1.0, ('/'.join(list(solve(st)))))
    #############################################################################

'''GUI的启动方法'''
def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

'''GUI启动'''
gui_start()
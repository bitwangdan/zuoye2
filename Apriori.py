#-*- coding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
class Apriori(object):
    def __init__(self, filename, min_support, min_confidence, item_start, item_end):
        self.filename = filename
        self.min_support = min_support # 最小支持度
        self.min_confidence = min_confidence
        self.line_num = 0 # item的行数
        self.item_start = item_start #  取哪行的item
        self.item_end = item_end
        self.location = [[i] for i in range(self.item_end - self.item_start + 1)]
        self.support = self.sut(self.location)
        print("the number of times ：", self.support)
        self.support_1 = self.support
        self.num = list(sorted(set([j for i in self.location for j in i])))# 记录item
        self.pre_support = [] # 保存前一个support,location,num
        self.pre_location = []
        self.pre_num = []
        self.item_name = [] # 项目名
        self.lift_list = []#每一个元素都是一条记录[[left], [right], support, confidence, lift]，用于去冗余以及绘图
        self.find_item_name()
        self.loop()
        #self.confidence_sup()

    def deal_line(self, line):
        "提取出需要的项"
        return [i.strip() for i in line.split('\t') if i]#[self.item_start - 1:self.item_end]
    def find_item_name(self):
        "根据第一行抽取item_name"
        with open(self.filename, 'r') as F:
            for index,line in enumerate(F.readlines()):
                if index == 0:
                    self.item_name = self.deal_line(line)
                    break
    def sut(self, location):
        """
        输入[[1,2,3],[2,3,4],[1,3,5]...]
        输出每个位置集的support [123,435,234...]
        """
        with open(self.filename, 'r') as F:
            support = [0] * len(location)
            for index,line in enumerate(F.readlines()):
                if index == 0: continue
                # 提取每信息
                item_line = self.deal_line(line)
                
                for index_num,i in enumerate(location):# 0 [0],1 [1], 2 [2]...
                    flag = 0
                    for j in i:
                        if item_line[j] != 'T':
                            flag = 1
                            break
                    if not flag:
                        support[index_num] += 1
            self.line_num = index # 一共多少行,除去第一行的item_name
        return support
    def select(self, c):
        "返回位置"
        stack = []
        for i in self.location:
            for j in self.num:
                if j in i:
                    if len(i) == c:
                        stack.append(i)
                else:
                    stack.append([j] + i)
        # 多重列表去重
        import itertools
        s = sorted([sorted(i) for i in stack])
        location = list(s for s,_ in itertools.groupby(s))
        return location
    def del_location(self, support, location):
        "清除不满足条件的候选集"
        # 小于最小支持度的剔除
        for index,i in enumerate(support):
            if i < self.line_num * self.min_support / 100:
                support[index] = 0
        # apriori第二条规则,剔除
        for index,j in enumerate(location):
            sub_location = [j[:index_loc] + j[index_loc+1:]for index_loc in range(len(j))]
            flag = 0
            for k in sub_location:
                if k not in self.location:
                    flag = 1
                    break
            if flag:
                support[index] = 0
        # 删除没用的位置
        location = [i for i,j in zip(location,support) if j != 0]
        support = [i for i in support if i != 0]
        return support, location
    def loop(self):
        "s级频繁项级的迭代"
        s = 2
        while True:
            print('-'*80)
            print('The' ,s - 1,'loop')
            print('location' , self.location)
            print('support' , self.support)
            print('confidence' , self.confidence_sup())#add confidence_sup
            print('num' , self.num)
            print('-'*80)
            # 生成下一级候选集
            location = self.select(s)
            support = self.sut(location)
            support, location = self.del_location(support, location)
            num = list(sorted(set([j for i in location for j in i])))
            s += 1
            if  location and support and num:
                self.pre_num = self.num
                self.pre_location = self.location
                self.pre_support = self.support
                self.num = num
                self.location = location
                self.support = support
            else:
                break
    def confidence_sup(self):
        "计算confidence"
        if sum(self.pre_support) == 0:
            print('min_support error') # 第一次迭代即失败
        else:
            for index_location,each_location in enumerate(self.location):
                del_num = [each_location[:index] + each_location[index+1:] for index in range(len(each_location))] # 生成上一级频繁项级
                del_num = [i for i in del_num if i in self.pre_location] # 删除不存在上一级频繁项级子集
                del_support = [self.pre_support[self.pre_location.index(i)] for i in del_num if i in self.pre_location] # 从上一级支持度查找
                # print del_num
                # print self.support[index_location]
                # print del_support
                for index,i in enumerate(del_num): # 计算每个关联规则支持度和自信度
                    left = []
                    right = []
                    index_support = 0
                    if len(self.support) != 1:
                        index_support = index
                    support =  float(self.support[index_location])/self.line_num # 支持度
                    s = [j for index_item,j in enumerate(self.item_name) if index_item in i]
                    left = i
                    right = each_location[index]
                    #print("s",s)
                    if del_support[index]:
                        confidence = float(self.support[index_location])/del_support[index] * 100
                        if confidence > self.min_confidence:
                            lift = confidence / self.support_1[each_location[index]]
                            print(','.join(s) , '->>' , self.item_name[each_location[index]] , \
                                ' min_support: ' , str(support) + '%' , \
                                ' min_confidence:' , str(confidence) + '%')
                            self.lift_list.append([left, right, support, confidence, lift])
        #print("successfully!")
def main():
    c = Apriori('data_result.txt', 24, 50 ,1, 8)
if __name__ == '__main__':
    main()

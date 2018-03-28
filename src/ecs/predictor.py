# coding=utf-8
import datetime
from ploynome import *
from GetInTheBox import *

def predict_vm(ecs_lines, input_lines):

    def DateSub(today, lastday):

        today = today.split('-')
        lastday = lastday.split('-')

        tY = int(today[0])
        tM = int(today[1])
        tD = int(today[2])

        lY = int(lastday[0])
        lM = int(lastday[1])
        lD = int(lastday[2])

        d1 = datetime.datetime(tY, tM, tD)
        d2 = datetime.datetime(lY, lM, lD)
        return (d1 - d2).days

    result = []

    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result

    #此处开始处理数据逻辑

    PhyMachineConf = input_lines[0].split() #第一行配置
    phyCpu = PhyMachineConf[0] #CPU核数
    phyMem = PhyMachineConf[1] #内存大小
    phyCpu = int(phyCpu)
    phyMem = int(phyMem)*1024

    TypeNum = int(input_lines[2]) #第三行预测虚拟机种类
    flavorType = [] #保存要预测虚拟机的种类，str类型
    for i in xrange(3, (3+TypeNum)):
        flavorType.append(input_lines[i].split()[0])
    print "flavorType:",flavorType

    predictType = input_lines[4+TypeNum] #预测的类型，CPU还是内存

    startDate = input_lines[-2].split()[0] #预测开始日子
    endDate = input_lines[-1].split()[0] #结束日子

    sumDate = DateSub(endDate, startDate) #统计要预测的天数

    flavorDict = {} #字典用来统计每种虚拟机请求个数
    for i in xrange(len(flavorType)): #初始化字典，加入相应键值
        if flavorType[i] not in flavorDict:
            flavorDict[flavorType[i]] = i

    flavorListTmp = [0 for i in xrange(len(flavorType))] #用于统计每天的数据

    BeginDay = ecs_lines[0].split()[2] #训练数据开始日期
    EndDay = ecs_lines[-1].split()[2] #训练数据结束日期
    lastCreatTime = BeginDay
    trainDate = DateSub(EndDay, BeginDay)
    flavorList = []  #用于统计训练数据

    for line in ecs_lines:
        #这里出来的是[[flavor1numbers,flavor2numbers,flavor3numbers],[...],[...]],len等于训练数据的天数
        values = line.split()
        flavorName = values[1]
        creatTime = values[2]

        caldate = DateSub(creatTime, lastCreatTime)
        for i in xrange(0, caldate):  # 判断非连续天数，补0
            flavorList.append(flavorListTmp)
            flavorListTmp = [0 for i in xrange(len(flavorType))]

        lastCreatTime = creatTime

        if flavorName in flavorType:
            #flavorDict[flavorName] += 1
            flavorListTmp[flavorDict[flavorName]] += 1

    for i in range(0, DateSub(startDate, EndDay)):
        flavorList.append(flavorListTmp)
        flavorListTmp = [0 for i in range(len(flavorType))]
    #print len(flavorList)
    #转置一下将flavor规格变成行数
    final_flavorList = transposition(flavorList)

    """在此之前完成数据处理
    第一阶段开始：预测
    """

    #对每个规格放进ploy模型
    M = 3 #多项式阶数
    flavor_pre = []
    for flavor_index,train_flavor in enumerate(final_flavorList):
        print "第%s个规格\n"%flavor_index
        pre_values = []
        X = [i+1 for i in xrange(len(train_flavor))]
        Y = []
        #Y需要贴合格式
        for y in train_flavor:
            s = []
            s.append(float(y))
            Y.append(s)

        #处理异常点
        Y = exception(Y)

        #现在是递归的做法，就是始终预测下一天
        for pre_date in xrange(sumDate):
            #更新X
            X = [i + 1 for i in xrange(len(train_flavor))]
            for i in xrange(len(X)):
                X[i] +=pre_date
            X_pre = X[-1]+1

            onePre_value = ploy_predictor(X,Y,M,X_pre)
            real_Pre_value = abs(onePre_value - Y[-1][0])
            pre_values.append(round(real_Pre_value))
            #更新Y
            del Y[0]
            ss = []
            ss.append(onePre_value)
            Y.append(ss)

        flavor_pre.append(pre_values)#所有的预测值，行数是对应规格字典的规格索引

    """第二阶段开始：分配"""
    getin(flavor_pre,flavorType,phyCpu,phyMem,predictType)
    result = getting_result()
    return result

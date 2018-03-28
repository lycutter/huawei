# -*- coding: utf-8 -*-
import re
"""本算法可以理解为递减首适应算法（对一维装箱问题效果好）"""

#虚拟机集合原始数据，从1号排到15号虚拟机规格
machine_num_origin = [0]*15

#统计虚拟机集合原始数据
def machine_num_count(flavor_pre,flavorType):
    if len(flavor_pre) == len(flavorType):
        for index,flavor_values in  enumerate(flavor_pre):
            sum = 0
            for one_value in flavor_values:
                sum += one_value

            flavor_name = flavorType[index]
            flavor_index = int(re.search(r'[0-9]+',flavor_name).group())
            machine_num_origin[flavor_index-1] = sum
    else:
        print "预测出来的规格数不对"


#处理后的虚拟机集合
machine_num = []
# 虚拟机规格（公开）
machine_map = [[1, 1024],
               [1, 2048],
               [1, 4096],
               [2, 2048],
               [2, 4096],
               [2, 8192],
               [4, 4096],
               [4, 8192],
               [4, 16384],
               [8, 8192],
               [8, 16384],
               [8, 32768],
               [16, 16384],
               [16, 32768],
               [16, 65536]
               ]
#rate是对应规格的cpu与内存的比，分三级，从cpu大到小排
rate_map = [[15,12,9,6,3],[14,11,8,5,2],[13,10,7,4,1]]

# 物理服务器集合
phy_machine = []
# 物理服务器节点(优化点：可以改用字典)
phy_machine_node = []
#cpu = 56
#mem = 131072
#cpuormem = 'mem'

def map_sort(rate_map,cpuormem):
    #如果优化cpu，则将性价比按cpu占比从高到低排
    if cpuormem == 'cpu':
        rate_map.reverse()
    #重新排序形成有优先级的虚拟机集合
    """
    #按三种优先级排，性价比(价值)分别是1024,2048,4096
    for level in rate_map:
        for n in level:
            norms = []
            norms.append(n)
            s = machine_num_origin[n-1]
            norms.append(s)
            machine_num.append(norms)
    print machine_num
    #利用率在75%左右，23个物理
    """

    #直接按规格从大到小排序，即15到1
    for index,num in enumerate(machine_num_origin):
        nurm = []
        nurm.append(index+1)
        nurm.append(num)
        machine_num.append(nurm)
    machine_num.reverse()


def phy_machine_node_init(phy_machine_node,cpu,mem):
    #初始化物理节点，0号储存cpu，1号储存men,2号存放规格1，以此类推，16号存放规格15
    phy_machine_node.append(cpu)
    phy_machine_node.append(mem)
    phy_machine_node.extend([0]*15)

def phy_machine_init(phy_machine):
    # 初始化物理服务器
    if len(phy_machine)== 0 :
        p_n = phy_machine_node[:]
        phy_machine.append(p_n)

def Myupdate(p_node, m_num,index):
    #判断条件：不能超分
    while m_num > 0 and p_node[0] >= machine_map[index][0] and p_node[1] >= machine_map[index][1]:
        #更新物理服务器
        p_node[0] -= machine_map[index][0]
        p_node[1] -= machine_map[index][1]
        #加2是因为cpu和内存在0,1位置
        p_node[index+2] += 1
        # 更新虚拟机集合
        m_num -= 1
    return m_num

def distribution(machine_num, phy_machine):
    # 检索每一种虚拟机规格的相应数量并从大到小放入
    for m_index,m_num in machine_num:
        m_index -= 1
        if m_num > 0:
            p_len = len(phy_machine)
            # 检索每一个物理节点
            for p_index in xrange(p_len):
                #比较的是CPU
                if phy_machine[p_index][0] > 0:
                    m_num = Myupdate(phy_machine[p_index], m_num,m_index)
                    if m_num == 0:
                        break

            # 上一个物理服务器满了，需要新建一个并放入
            while m_num >0:
                p_n = phy_machine_node[:]
                m_num = Myupdate(p_n, m_num,m_index)
                phy_machine.append(p_n)
"""
def output_data(cpu,phy_machine):
    all_using_rate = 0.0
    #按格式输出
    print len(phy_machine)
    for index, p_node in enumerate(phy_machine):
        outword = ""
        outword += str(index+1) + ' '
        for inside_index,p_num in enumerate(p_node[2:]):
            if p_num != 0:
                outword += "flavor%s"%(inside_index+1) + ' ' + str(p_num)+' '
        using_rate = (phy_machine_node[0]-p_node[0])/(cpu*1.00)
        all_using_rate += using_rate
        outword += "资源利用率：%s"%(using_rate*100) +' '
        outword += "剩余CPU：%s"%p_node[0] + ' '
        outword += "剩余内存：%s"%p_node[1]
        print outword
    #总利用率
    all_using_rate *= 100
    all_using_rate /= len(phy_machine)
    print "总资源利用率：%s"%(all_using_rate)
"""

def getting_result():
    result = []

    #虚拟机预测总数
    all_machine_num = 0
    for numbers in machine_num_origin:
        all_machine_num += numbers
    result.append(str(int(all_machine_num)))

    #虚拟机具体预测情况
    for num_index, numbers in enumerate(machine_num_origin):
        outword = ""
        if numbers != 0:
            outword += 'flavor%s %s' % (num_index + 1, int(numbers))
            result.append(outword)

    result.append(" ")
    result.append(len(phy_machine))

    #物理机情况
    for index, p_node in enumerate(phy_machine):
        outword = ""
        outword += str(index+1) + ' '
        for inside_index,p_num in enumerate(p_node[2:]):
            if p_num != 0:
                outword += "flavor%s"%(inside_index+1) + ' ' + str(p_num)+' '
        result.append(outword)
    return result


def getin(flavor_pre,flavorType,cpu,mem,cpuormem):

    machine_num_count(flavor_pre, flavorType)
    map_sort(rate_map,cpuormem)
    phy_machine_node_init(phy_machine_node, cpu, mem)
    phy_machine_init(phy_machine)
    #分配
    distribution(machine_num, phy_machine)
    #output_data(cpu,phy_machine)

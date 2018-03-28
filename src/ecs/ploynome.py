# -*- coding:utf-8 -*-
import math
def transposition(array):
    #求转置矩阵
    x_a = len(array)
    y_a = len(array[0])
    b = [[0]*x_a for i in xrange(y_a)]
    for x in xrange(x_a):
        for y in xrange(y_a):
            b[y][x] = array[x][y]
    #print "转置矩阵：",b
    return b

def array_mult(array1,array2 = None,parameter = 0):
    if array1 is None and array2 is None:
        print "矩阵相乘输入空"
        return [0]
    c = []
    if parameter == 0 :
        #矩阵相乘
        x_a = len(array1)#a矩阵的行数
        y_a = len(array1[0])#a矩阵的列数
        x_b = len(array2)
        y_b = len(array2[0])
        if y_a == x_b:
            for x in xrange(x_a):
                c_x = []
                for y in xrange(y_b):
                    sum = 0.0
                    for x1 in xrange(x_b):
                        sum += array1[x][x1]*array2[x1][y]
                    c_x.append(sum)
                c.append(c_x)
            #print "两个矩阵乘积：",c
        else:
            print "行列不匹配"
    else:
        #c = [[array1[x][y] for y in xrange(len(array1[0]))] for x in xrange(len(array1))]
        if array1 is not None:
            c = [[array1[x][y] for y in xrange(len(array1[0]))] for x in xrange(len(array1))]
        elif array2 is not None:
            c = [[array2[x][y] for y in xrange(len(array2[0]))] for x in xrange(len(array2))]
        x_a = len(c)
        y_a = len(c[0])
        for x in xrange(x_a):
            for y in xrange(y_a):
                c[x][y] *= parameter

    return c

def array_add(array1,array2):
    #矩阵相加
    if array1 is None and array2 is None:
        print "矩阵相加输入空"
        return [0]
    x_a = len(array1)  # a矩阵的行数
    y_a = len(array1[0])  # a矩阵的列数
    x_b = len(array2)
    y_b = len(array2[0])
    c = [[0]*y_a for i in xrange(x_a)]
    if x_a == x_b and y_a == y_b:
       for x in xrange(x_a):
           for y in xrange(y_a):
               c[x][y] = array1[x][y]+array2[x][y]
    else:
        print "（矩阵相加）两个矩阵不同维"
    return c

def determinant(array):
    sum = 0
    #行列式
    lenth = len(array)
    if lenth <= 2:
        if lenth == 2:
            sum = array[0][0]*array[1][1]-array[0][1]*array[1][0]
    else:
        #只求第一行的代数余子式，然后相加
        for y_index in xrange(lenth):
            #切分余子式
            array1 = [[array[x][y] for y in xrange(lenth)] for x in xrange(lenth)]
            del array1[0]
            for x in xrange(len(array1)):
                del array1[x][y_index]

            sum += (array[0][y_index]*determinant(array1))*pow(-1,y_index)
    return sum

def adjoint(array):
    #求伴随矩阵
    lenth = len(array)
    c = [[0]*lenth for i in xrange(lenth)]
    for x_index in xrange(lenth):
        for y_index in xrange(lenth):
            array1 = [[array[x][y] for y in xrange(lenth)] for x in xrange(lenth)]
            del array1[x_index]
            for x in xrange(len(array1)):
                del array1[x][y_index]
            #伴随矩阵的项,这里还没有转置了
            c[x_index][y_index] = determinant(array1)*pow(-1,x_index+y_index)

    return transposition(c)

def array_inverse(array):
    #矩阵求逆
    x_a = len(array)
    y_a = len(array[0])
    if x_a == y_a:
        #用伴随矩阵求逆
        adj = adjoint(array)
        det = determinant(array)
        for x in xrange(x_a):
            for y in xrange(y_a):
                adj[x][y] /= det
        return adj
    else:
        print "求逆不是方阵"
        return []

def ploy(X,Y,M,U):
    #参数X应该是n维向量
    #参数Y应该是n维向量

    x_array = []
    #构造x矩阵，n行M列，n是x的项数
    for x_i in X:
        x_item = []
        for i in xrange(M+1):
            x_item.append(pow(x_i,i))
        x_array.append(x_item)
    #print "x_array:",x_array

    #正则化需要的单位矩阵
    I = [[0]*(M+1) for i in xrange(M+1)]
    for i in xrange(M+1):
        if i !=0:
            I[i][i] = 1

    #正则化系数

    #代入公式
    step1 = array_mult(transposition(x_array),x_array)
    step2 = array_mult(I, parameter = U)
    step3 = array_add(step1,step2)
    step4 = array_inverse(step3)
    step5 = array_mult(step4,transposition(x_array))
    step6 = array_mult(step5,Y)
    w =step6

    #历史值
    y_history = []
    for x_history in X:
        sum = 0.0
        for i in xrange(M + 1):
            sum += w[i][0] * pow(x_history, i)
        y_history.append(round(sum))

    return w



def calStd(y, avg):
    sum = 0.0
    for y_v in y:
        sum += math.pow((y_v[0] - avg), 2)
    sum = sum / len(y)
    calstd = math.sqrt(sum)
    return calstd




def exception(y):
    # 处理异常点
    sum = 0.0
    for y_v in y:
        y_value = y_v[0]
        sum += y_value
    avg = sum / (len(y))
    calstd = calStd(y, avg)
    std = avg + 2 * calstd
    for y_v in y:
        y_value = y_v[0]
        while y_value > std:
            y_v[0] -= avg
            y_value = y_v[0]

    # 叠加数据
    y_len = len(y)
    for i in xrange(y_len):
        if i + 1 < y_len:
            y[i + 1][0] += y[i][0]

    return y

def ploy_predictor(x,y,m,x_pre):
    # = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    #y = [[0.0],[11.0],[1.0],[0.0],[1.0],[0.0],[3.0],[0.0],[7.0],[0.0],[0.0],[0.0],[1.0],[0.0],[27.0]]
    #m = 4
    #x_pre = 16
    """
    RMSE_min  = 10
    #后验正则化系数
    U_min_index = 0
    for i in xrange(20):
        U = pow(2.72,i)
        w = ploy(x,y,m,U)
        for x_after in xrange(len(x)):
            sum = 0.0
            for i in xrange(m + 1):
                sum += w[i][0] * pow(x_after, i)
            RMSE = y[x_after][0] - sum
            RMSE = -RMSE if RMSE<0 else RMSE
            if RMSE<RMSE_min:
                RMSE_min = RMSE
                U_min_index = i
    U = pow(2.72,U_min_index)
    """
    U = 50
    # 求权重
    w = ploy(x,y,m,U)
    #代入公式
    sum = 0.0
    for i in xrange(m+1):
        sum +=w[i][0]*pow(x_pre,i)

    return sum

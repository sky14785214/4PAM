# from tkinter import Y
import numpy as np
import matplotlib.pyplot as plt
numTrans = 10
d = 1
encodedInput = np.zeros((numTrans,1), dtype=float)# 存儲 10,000 對輸入位的星座映射值的矩陣
input = np.zeros((2*numTrans,), dtype=int) # 在這種情況下，存儲 10,000 次傳輸的矩陣，每次傳輸 2 個隨機位
# input = [0,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,0,0,1,1]


def Random_2bit(Number,d,encodedInput,input): # 隨機生成2位元亂數(資料數,d,encodedintput)
    
    temp = np.random.randint(2,size=Number*2)
    bit = 0
    for i in range(0,Number,1):
        inputSymbol = 0
        if (temp[bit:bit+2] == [0,0]).all(): # 遍歷輸入的傳輸序列
            inputSymbol = -3*d
        elif (temp[bit:bit+2] == [0,1]).all():
            inputSymbol = -d
        elif (temp[bit:bit+2] == [1,1]).all():
            inputSymbol = d
        elif (temp[bit:bit+2] == [1,0]).all():
            inputSymbol = 3*d

        bit = bit + 2
        encodedInput[i] = inputSymbol
        input = temp

        # Ans.append(inputSymbol)  # 將獲得的值存儲在適當的矩陣中

    
    return encodedInput,input



encodedInput,input = Random_2bit(numTrans,1,encodedInput,input) # 隨機生成2位元亂數

# print(input)
t = np.linspace( 0, 1, 2000, endpoint = False ) # 定義時間陣列
    
x = np.cos( 2 * np.pi * 1 * t ) * 0.9                # 產生弦波
y = np.cos( 2 * np.pi * 1 * t ) * 0.45
# z = np.cos( 2 * np.pi * 1 * t + 90 * np.pi / 180.0 ) * 1
# x1 = np.cos( 2 * np.pi * 1 * t + 180 * np.pi / 180.0) * 0.9
# y1 = np.cos( 2 * np.pi * 1 * t + 180 * np.pi / 180.0) * 0.45

# x2 = np.cos( 2 * np.pi * 1 * t + 270 * np.pi / 180.0) * 0.9
# y2 = np.cos( 2 * np.pi * 1 * t + 270 * np.pi / 180.0) * 0.45

# z = 1.35
# z1 = -1.35

a = x*0 + y*0 
b = x*0 + y*1
c = x*1 + y*1
d = x*1 + y*0

# e = x1*0 + y1*0 
# f = x1*0 + y1*1
# g = x1*1 + y1*1
# h = x1*1 + y1*0


# i = x2*0 + y2*0 
# j = x2*0 + y2*1
# k = x2*1 + y2*1
# l = x2*1 + y2*0

# a = x + x90
plt.plot( t,a ,t,b, t,c, t,d, )  
# plt.plot( t,a ,t,b, t,c, t,d, t,e, t,f, t,g, t,g, )                               # 繪圖
# plt.plot( t, x , t,y )
plt.xlabel( 't (second)' )
plt.ylabel( 'Amplitude' )
plt.axis( [ 0, 1, -1.8, 1.8 ] )

plt.show( )

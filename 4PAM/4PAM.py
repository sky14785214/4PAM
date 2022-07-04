# 4-PAM 數字通信系統建模

from multiprocessing.dummy import Array
import numpy as np
import cmath
import math
import matplotlib.pyplot as plt
import pandas as pd

numTrans = 10000
# SNR = 0 
d = 1

input = np.zeros((2*numTrans,), dtype=int) # 在這種情況下，存儲 10,000 次傳輸的矩陣，每次傳輸 2 個隨機位
encodedInput = np.zeros((numTrans,1), dtype=float)# 存儲 10,000 對輸入位的星座映射值的矩陣
encodedOutput = np.zeros((numTrans,1), dtype=float)# 通過噪聲通道傳輸後存儲值的矩陣
output = np.zeros((2*numTrans,1), dtype=float)# 存儲解碼後獲得的比特對的矩陣
ArraySNR = [0,2,4,6,8,10,12,15]  #  8 個不同的 SNR 值，以 dB 為單位
pBitError = np.zeros((8,1), dtype=float) # 每個 SNR 值的誤碼概率
simulatedSER = np.zeros((8,1), dtype=float) # 每個 SNR 值的模擬誤碼概率
simulatedBER = np.zeros((8,1), dtype=float) # 每個 SNR 值的模擬符號錯誤概率
theorySER = np.zeros((8,1), dtype=float) # 推導每個 SNR 值的誤碼概率
theoryBER = np.zeros((8,1), dtype=float) # 每個 SNR 值的符號錯誤概率

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

def AWGN(numTrans,snrLinear): # 通過 AWGN 信道傳輸
    noisyOutput = np.zeros((1,numTrans), dtype=float)
    temp = np.zeros((1,numTrans), dtype=float)
    
    v = 5 / (4*snrLinear)
    noiseSamples = cmath.sqrt(v)*np.random.randn(numTrans,1) # 生成與傳輸次數一樣多的真實（I 軸）AWGN 樣本

    noisyOutput = encodedInput + noiseSamples # 向通過通道傳輸的信號添加噪聲
    # print("encodedInput: ",encodedInput)
    # print("encodedInputlen: ",len(encodedInput))
    # print("noisyOutput:",noisyOutput)
    return noisyOutput

def DetectorModelling(numTrans,noisyOutput,encodedOutput):
    outputSymbol = 0
    # print(len(noisyOutput))
    for i in range(0,numTrans,1): #遍歷有噪聲的信號值，並為有噪聲的星座值分配適當的級別
        # print(noisyOutput[i])
        if noisyOutput[i]>0: # 正值解碼
            if noisyOutput[i]>3*d:
                outputSymbol = 3*d
            elif (noisyOutput[i]<3*d) & (noisyOutput[i]>2*d):
                outputSymbol = 3*d
            else:
                outputSymbol = d
        elif noisyOutput[i]<0: # 負值解碼
            if noisyOutput[i]<-3*d:
                outputSymbol = -3*d
            elif (noisyOutput[i]>-3*d) & (noisyOutput[i]<-2*d):
                outputSymbol = -3*d
            else:
                outputSymbol = -d
        encodedOutput[i] = outputSymbol # 將獲得的值存儲在適當的矩陣中
    return encodedOutput

def Decoding(numTrans,encodedOutput,output,d): #解碼
    q = 0
    for i in range(0,numTrans,1):
        if encodedOutput[i] == 3*d: # 為每個值分配適當的位對
            # output[q:q+2] = [1,0]
            output[q] = 1
            output[q+1] = 0
        elif encodedOutput[i] == d:
            # output[q:q+2] = [1,1]
            output[q] = 1
            output[q+1] = 1
        elif encodedOutput[i] == -d:
            # output[q:q+2] = [0,1]
            output[q] = 0
            output[q+1] = 1
        elif encodedOutput[i] == -3*d:
            # output[q:q+2] = [0,0]
            output[q] = 0
            output[q+1] = 0
        q = q + 2
    # print("encodedOutput: ",encodedOutput)
    # print("output: ",output)
    return encodedOutput,output

def DetermineSymbolError(numTrans,encodedOutput,encodedInput,errorSymbols):
    for i in range(0,numTrans,1):
        if encodedOutput[i] != encodedInput[i]:
            errorSymbols = errorSymbols + 1
    # print(errorSymbols)
    return errorSymbols

def DetermineBitError(numTrans,output,input,errorBits): #確定位錯誤
    for i in range(0,numTrans*2,1): # 遍歷位的輸入和輸出組合併記錄它們之間的差異
        
        if output[i] != input[i]:
            errorBits = errorBits + 1
    print("errorBits: ",errorBits)
    return errorBits

def qfunc(t):
	return 0.5-0.5*math.erf(t/math.sqrt(2.))





for SNR in range(0,len(ArraySNR),1):
    d = 1
    errorBits = 0; # 用於計算解碼後錯誤位數的變量
    errorSymbols = 0; # 用於計算符號錯誤數量的變量
    snrLinear = 10**(ArraySNR[SNR]/10) # 每個 SNR 值的線性值

    encodedInput,input = Random_2bit(numTrans,1,encodedInput,input) # 隨機生成2位元亂數
    noisyOutput = AWGN(numTrans,snrLinear) # 通過 AWGN 信道傳輸
    encodedOutput= DetectorModelling(numTrans,noisyOutput,encodedOutput) # 探測器建模
    encodedOutput,output = Decoding(numTrans,encodedOutput,output,d) # 解碼
    errorSymbols = DetermineSymbolError(numTrans,encodedOutput,encodedInput,errorSymbols)
    errorBits= DetermineBitError(numTrans,output,input,errorBits)
    # print(SNR)

    simulatedBER[SNR] = errorBits / (2*numTrans) # 模擬的誤碼率

    simulatedSER[SNR] = errorSymbols / numTrans #模擬的 符號錯誤率

    theorySER[SNR] = (3/2)* qfunc(math.sqrt((4/5)*snrLinear)) # 符號錯誤值的理論概率
    
    theoryBER[SNR] = theorySER[SNR] / math.log(4,2); # B由於輸入數據的格雷碼編碼，BER 是 SER 除以系統維度的以 2 為底的 log
# print("theoryBER[SNR]: ",theoryBER)  
# print("simulatedBER: ",simulatedBER)   
print("theorySER: ",theorySER)



plt.plot(ArraySNR, simulatedBER, color='b', label='simulatedBER')
plt.plot(ArraySNR, theorySER, 'r', label='theorySER')
# plt.scatter(ArraySNR, theorySER, 'r', label='theorySER')
plt.xlabel('Average SNR per bit (dB)') # 設定x軸標題 每比特平均 SNR (dB)
plt.ylabel('Probability of bit error') # 誤碼率 
plt.xticks(ArraySNR, rotation='vertical') # 設定x軸label以及垂直顯示 
plt.title('Bit error probability curve for 4-PAM') # 設定圖表標題 4-PAM 的誤碼概率曲線
plt.legend(loc = 'lower left')
plt.axis([15,0,1,1e-5])
plt.show()


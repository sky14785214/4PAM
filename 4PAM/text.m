% 4-PAM 數字通信系統建模
numTrans = 10000; % 傳輸次數
input = zeros(1, 2*numTrans); %在這種情況下，存儲 10,000 次傳輸的矩陣，每次傳輸 2 個隨機位
encodedInput = zeros(1, numTrans); % 存儲 10,000 對輸入位的星座映射值的矩陣
encodedOutput = zeros(1, numTrans); % 通過噪聲通道傳輸後存儲值的矩陣
output = zeros(1, 2*numTrans); % 存儲解碼後獲得的比特對的矩陣

snr = [0 2 4 6 8 10 12 15]; %  8 個不同的 SNR 值，以 dB 為單位
pBitError = zeros(1,8); % 每個 SNR 值的誤碼概率
d = 1; % 假設 d = 1
simulatedSER = zeros(1,8); % 每個 SNR 值的模擬誤碼概率
simulatedBER = zeros(1,8); % 每個 SNR 值的模擬符號錯誤概率
theorySER = zeros(1,8); % 推導每個 SNR 值的誤碼概率
theoryBER = zeros(1,8); % 每個 SNR 值的符號錯誤概率
for s = 1:8
    i = 1; % 重置變量以遍歷矩陣
    j = 1;
    k = 1;
    n = 1;
    q = 1;
    errorBits = 0; % 用於計算解碼後錯誤位數的變量
    errorSymbols = 0; % 用於計算符號錯誤數量的變量
    snrLinear = 10^(snr(s)/10); % 每個 SNR 值的線性值

    % 信息源建模

    % 在矩陣中輸入隨機位組合
    while i <= 2*numTrans 

        twoBits = round(rand(1, 2)); % 隨機位生成器，用於 0 和 1 概率相等的一對位

        input(i:i+1) = twoBits;
        i = i + 2;
    end
    %  編碼
    while k < numTrans 
    % 遍歷輸入的傳輸序列

        if input(j:j+1) == [0 0] % 遍歷輸入的傳輸序列
            inputSymbol = -3*d;
        elseif input(j:j+1) == [0 1]
            inputSymbol = -d;
        elseif input(j:j+1) == [1 1]
            inputSymbol = d;
        elseif input(j:j+1) == [1 0]
            inputSymbol = 3*d;
        end
        j = j + 2;
        encodedInput(k) = inputSymbol; % 將獲得的值存儲在適當的矩陣中
        k = k + 1;

    end

    v = 5 / (4*snrLinear);

    % 通過 AWGN 信道傳輸

    noiseSamples = sqrt(v)*randn(1,numTrans); % 生成與傳輸次數一樣多的真實（I 軸）AWGN 樣本

    noisyOutput = encodedInput + noiseSamples; % 向通過通道傳輸的信號添加噪聲


    % 探測器建模
    for m = 1:numTrans % 遍歷有噪聲的信號值，並為有噪聲的星座值分配適當的級別


        if noisyOutput(m)>0 % 正值解碼

            if noisyOutput(m)>3*d 
                outputSymbol = 3*d;
            elseif(noisyOutput(m)<3*d) && (noisyOutput(m)>2*d) 
                outputSymbol = 3*d;
            else
                outputSymbol = d;
            end
        elseif noisyOutput(m)<0 % 負值解碼
            if noisyOutput(m)<-3*d
                outputSymbol = -3*d;
            elseif (noisyOutput(m)>-3*d) && (noisyOutput(m)<-2*d) 
                outputSymbol = -3*d;
            else
                outputSymbol = -d;
            end
        end
        encodedOutput(m) = outputSymbol; % 將獲得的值存儲在適當的矩陣中
    end

    % % 解碼
    while n < numTrans % Iterate through noisy output constellation values

    if encodedOutput(n) == 3*d % 為每個值分配適當的位對
        output(q:q+1) = [1 0];
    elseif encodedOutput(n) == d
        output(q:q+1) = [1 1];
    elseif encodedOutput(n) == -d
        output(q:q+1) = [0 1];
    elseif encodedOutput(n) == -3*d
        output(q:q+1) = [0 0];
    end

    q = q + 2;
    n = n + 1;

    end
    % 確定符號錯誤

    for l = 1: numTrans 

        if encodedOutput(l) ~= encodedInput(l)
            errorSymbols = errorSymbols + 1;
        end 
    end

    % 確定位錯誤
    for r = 1:2*numTrans % 遍歷位的輸入和輸出組合併記錄它們之間的差異

        if output(r) ~= input(r)
            errorBits = errorBits + 1;  
        end
    end

    simulatedBER(s) = errorBits / (2*numTrans);

    simulatedSER(s) = errorSymbols / numTrans;

    theorySER(s) = (3/2)* qfunc(sqrt((4/5)*snrLinear)); % 符號錯誤值的理論概率
    theoryBER(s) = theorySER(s) / log2(4); % B由於輸入數據的格雷碼編碼，BER 是 SER 除以系統維度的以 2 為底的 log
    disp(theoryBER(s));
end
    % 圖表的情節
    figure;
    semilogy(snr, theoryBER);
    hold on;
    semilogy(snr, simulatedBER, 'ro');
    axis([0 15 1e-5 1]);
    xlabel('每比特平均 SNR (dB)');
    ylabel('誤碼率');
    title('4-PAM 的誤碼概率曲線');
    legend('理論', '模擬');
 
% End of code
import pywt
from enum import Enum
import numpy as np
from dialog import InputNumber

class CWT_Setting:
    class Key(Enum):
        WaveletName = "WaveletName"
        Scales = "Scales"
    
    WaveletName = 0
    Scales = 0
    Keys = ["WaveletName", "Scales"]
    
    def __Init__():
        pass  # 初始化（如果沒有特別要初始化的內容，可以用 pass）
    
    def ChoiceDialog():
        print("Choice Continuous Wavelet Transform wave")
        print("(1)morl, 適合時頻分析，頻率選擇性較好，常用於時頻解析")
        print("(2)mexh, 二階導數 Gaussian，小波能量集中，適合邊緣檢測")
        print("(3)paul, 低頻響應較好，適合平滑變化的信號")
        print("(4)dog, 適合特徵檢測，例如 dog(2) 近似 mexh")
        print("(5)cgau1, 適合分析方波信號")
        print("(6)shan, 適合處理複數信號")
        print("(7)fbsp, 可調整形狀，適合不同類型的信號分析")
        
        wavelet_use = InputNumber("Plesase enter your choice: ")
        wavelets = ['morl', 'mexh', 'paul', 'dog', 'cgau1', 'shan', 'fbsp']

        if wavelet_use > len(wavelets) or wavelet_use <= 0 or wavelet_use == None:
            print("Your choice is bot supproted!")
            quit()

        n = InputNumber("Enter the scale: ")

        if n <= 0 or n == None:
            print("Your choice is bot supproted!")
            quit()
            
        fc_wavelet = pywt.central_frequency(wavelets[wavelet_use - 1])
        print(f"{wavelets[wavelet_use - 1]} central frequency = {fc_wavelet}")

        # 計算 CWT Scale 和對應頻率
        cparam = 2 * fc_wavelet * n
        scales = cparam / np.arange(n , 0, -1)
        
        CWT_Setting.WaveletName = wavelets[wavelet_use - 1]
        CWT_Setting.Scales = scales
        return {"WaveletName": wavelets[wavelet_use - 1], "Scales": scales}
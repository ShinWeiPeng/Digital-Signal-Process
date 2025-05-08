import pywt
from enum import Enum
import numpy as np
from dialog import InputNumber

class DWT_Setting:
    class Key(Enum):
        WaveletName = "WaveletName"
        Level = "Level"
        DecompositionFilterLen = "DecompositionFilterLen"
        ReconstructionFilterLen = "ReconstructionFilterLen"
    
    WaveletName = 0
    Level = 0
    Keys = ["WaveletName", "Level", "DecompositionFilterLen", "ReconstructionFilterLen"]
    
    def __Init__():
        pass  # 初始化（如果沒有特別要初始化的內容，可以用 pass）
    
    def ChoiceDialog():
        # 初始化濾波器長度和層數
        decomposition_filter_len = None
        reconstruction_filter_len = None
        level = None

        # 定義映射字典，將小波類型與名稱格式對應
        wavelet_name_format = {
            1: 'haar',  # Haar 小波
            2: 'db{level}',  # Daubechies 小波
            3: 'sym{level}',  # Symlets 小波
            4: 'bior{decomposition_filter_len}.{reconstruction_filter_len}',  # Biorthogonal 小波
            5: 'coif{level}'  # Coiflets 小波
        }
        
        print("Choice Continuous Wavelet Transform wave")
        print("(1)Haar, 適合快速變化或階段性信號，如信號中有快速變化或尖銳的邊界（例如突變或沖擊信號）。")
        print("(2)Daubechies, 適合快速變化或階段性信號，如信號中有快速變化或尖銳的邊界（例如突變或沖擊信號)。")
        print("(3)Symlets, 適合平滑或對稱性要求高的信號，如圖像處理。")
        print("(4)Biorthogonal, 適合信號重建與去噪")
        print("(5)Coiflets, 適合高解析度的平滑信號")

        wavelet_use = InputNumber("Plesase enter your choice: ")
        
        if wavelet_use > len(wavelet_name_format) or wavelet_use <= 0 or wavelet_use == None:
            print("Your choice is bot supproted!")
            quit()

        if wavelet_use == 4:
            decomposition_filter_len = InputNumber("Enter the decomposition filter len: ")
            reconstruction_filter_len = InputNumber("Enter the reconstruction filter len: ")
            
            if decomposition_filter_len <= 0 or decomposition_filter_len == None:
                print("Your choice is bot supproted!")
                quit()
                
            if reconstruction_filter_len <= 0 or reconstruction_filter_len == None:
                print("Your choice is bot supproted!")
                quit()
                
            wavelet_name = wavelet_name_format[wavelet_use].format(
                decomposition_filter_len = decomposition_filter_len, 
                reconstruction_filter_len = reconstruction_filter_len
            )
        elif wavelet_use == 1:
            level = 1
            wavelet_name = wavelet_name_format[wavelet_use]
        else:
            level = InputNumber("Enter the level: ")

            if level <= 0 or level == None:
                print("Your choice is bot supproted!")
                quit()
                
            wavelet_name = wavelet_name_format[wavelet_use].format(level = level)
        
        DWT_Setting.WaveletName = wavelet_name
        DWT_Setting.Level = level
        print(f"wavelet_name = {wavelet_name}")
        return {
            "WaveletName": wavelet_name, 
            "Level": level, 
            "DecompositionFilterLen": decomposition_filter_len, 
            "ReconstructionFilterLen": reconstruction_filter_len 
        }
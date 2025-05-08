
import csv
import tkinter as tk
from tkinter import filedialog
import numpy as np
from enum import Enum
from pathlib import Path

TIME = 0
X_AXIS = 1
Y_AXIS = 2
Z_AXIS = 3

DATA_OFFSET = 1

class ReadAccCsv:
    class Key(Enum):
        ACC_X = "AccX"
        ACC_Y = "AccY"
        ACC_Z = "AccZ"
        FILE_NAME = "FileName"

    Keys = ["AccX", "AccY", "AccZ", "FileName"]

    def __Init__():
        pass  # 初始化（如果沒有特別要初始化的內容，可以用 pass）

    def Read():
        # print(f"Available Keys: {ReadAccCsv.Keys}")
        
        # 創建 Tkinter 視窗，但不顯示
        root = tk.Tk()
        root.withdraw()  # 隱藏主視窗

        # 讓使用者選擇資料夾
        # folder_path = filedialog.askdirectory(title="選擇資料夾")

        # 如果使用者未選擇資料夾，則結束程式
        # if not folder_path:
        #     print("未選擇資料夾，程式結束")
        #     exit()

        # 讓使用者選擇檔案
        file_path = filedialog.askopenfilename(
            title="選擇 CSV 檔案",
            # initialdir=folder_path,  # 設定初始目錄為剛選擇的資料夾
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        # 如果使用者未選擇檔案，則結束程式
        if not file_path:
            print("未選擇檔案")
            return None

        file_name = Path(file_path).name
        
        # 讀取 CSV 檔案
        with open(file_path, newline='', encoding='utf-8') as cavDataFile:
            reader = csv.reader(cavDataFile)
            data_x = []
            data_y = []
            data_z = []
            for row in reader:
                data_x.append(row[X_AXIS])
                data_y.append(row[Y_AXIS])
                data_z.append(row[Z_AXIS])

        # 轉換數據
        acc_x = [eval(data_x[i]) for i in range(DATA_OFFSET, len(data_x))]  
        acc_y = [eval(data_y[i]) for i in range(DATA_OFFSET, len(data_y))]  
        acc_z = [eval(data_z[i]) for i in range(DATA_OFFSET, len(data_z))]  
        
        acc_np_arr_x = np.array(acc_x)
        acc_np_arr_y = np.array(acc_y)
        acc_np_arr_z = np.array(acc_z)
        return {"AccX": acc_np_arr_x, "AccY": acc_np_arr_y, "AccZ": acc_np_arr_z, "FileName": file_name}
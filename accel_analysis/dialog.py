def __Init__():
    pass  # 初始化（如果沒有特別要初始化的內容，可以用 pass）

def InputNumber(prompt):
    while True:
        user_input = input(prompt).strip() # 除字串兩端的空白字符（包括空格、換行符、制表符等）

        if not user_input:
            print("No input provided.")
            return None  # 可依需求改為預設值，如 return 0 或 raise Exception

        try:
            value = float(user_input)  # 嘗試將輸入轉換為浮點數
            # 如果你希望強制返回整數
            if value.is_integer():
                return int(value)  # 如果是整數，返回整數型別
            return value  # 如果是浮點數，返回浮點數
        except ValueError:
            try:
                value = int(user_input)  # 如果無法轉換為浮點數，再嘗試轉換為整數
                return value
            except ValueError:
                print("既不是浮點數也不是整數")
                return None
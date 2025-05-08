class Test:
    class_var = 100  # 類別變數（所有實體共用）

    def __init__(self, value):
        self.instance_var = value  # 實體變數（每個物件自己有自己的）
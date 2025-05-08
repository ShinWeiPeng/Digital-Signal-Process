class Test:
    class_var = 100  # 類別變數（所有實體共用）

    def __init__(self, value):
        self.old = 0
        self.instance_var = value  # 實體變數（每個物件自己有自己的）
        
    def add(self, value):
        self.sum = value + self.instance_var
        
    def set_old_val(self, value):
        self.old = value
        
    def add_old(self):
        self.sum = self.old  + self.instance_var
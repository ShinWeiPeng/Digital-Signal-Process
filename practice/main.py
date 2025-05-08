from test_class import Test 

a = Test(10)
b = Test(20)

print(a.instance_var)  # 10
print(b.instance_var)  # 20

a.instance_var = 999
print(a.instance_var)  # 999
print(b.instance_var)  # 20 ← b不受影響

a.add(10)
b.add(10)
print(a.sum)  
print(b.sum)  

print(f"{a.old}") 
print(f"{a.old}") 

a.set_old_val(20)
b.set_old_val(50)

print(f"{a.old}") 
print(f"{b.old}") 

a.add_old()
b.add_old()

print(f"{a.sum}") 
print(f"{b.sum}") 
USERNAME = 'root'
PASSWORD = 'rootpassword'
localhost = 37017


import re

time = '12mo hieuee'

# Sử dụng regex để tìm kiếm số trong chuỗi
numbers = re.findall(r'\d+', time)
print(int(numbers[0]))
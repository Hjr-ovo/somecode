#课中小练
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(-99))


"""
练习
请定义一个函数 `quadratic(a, b, c)` ，接收3个参数，返回一元二次方程 $ax^2+bx+c=0$ 的两个解。

import math

def quadratic(a, b, c):
    pass

# 测试:
print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')

"""

import math

def quadratic(a, b, c):
    # 计算判别式
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return None  # 无实数解
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return (root1, root2)

# 测试:
print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')
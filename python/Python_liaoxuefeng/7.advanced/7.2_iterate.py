"""
练习
请使用迭代查找一个list中最小和最大值，并返回一个tuple：

def findMinAndMax(L):
    return (None, None)

# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
"""


def findMinAndMax(L):
    if not L:
        return (None, None)
    min_value = max_value = L[0]
    for num in L:
        if num < min_value:
            min_value = num
        elif num > max_value:
            max_value = num
    return (min_value, max_value)

# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
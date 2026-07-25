"""
使用key-value存储结构的dict在Python中非常有用，选择不可变对象作为key很重要，最常用的key是字符串。

tuple虽然是不变对象，但试试把(1, 2, 3)和(1, [2, 3])放入dict或set中，并解释结果。



"""

#以下没问题，因为key1是tuple，tuple是不可变类型，可以作为dict的key
dict = { "a": 1, "b": 2, "c": 3 }
key1 = (1, 2, 3)
dict[key1] = 4
print(dict)

#以下有问题，因为key2是tuple，但是tuple中包含了list，list是可变类型，不能作为dict的key
key2 = (1, [2, 3])
#dict[key2] = 4
'''
报错如下
Traceback (most recent call last):
  File "lesson6.py", line 12, in <module>
    dict[key2] = 4
    ~~~~^^^^^^
TypeError: unhashable type: 'list'
'''
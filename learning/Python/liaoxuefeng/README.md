# 🐍 Python 廖雪峰教程学习笔记

> 本目录用于记录学习廖雪峰 Python 教程的练习代码和笔记。

## 简介

廖雪峰的 Python 教程（[https://www.liaoxuefeng.com/](https://www.liaoxuefeng.com/)）是一套广受好评的 Python 入门教程，从基础语法到高级特性，涵盖了 Python 开发的方方面面。

本目录收录学习该教程过程中的练习题、示例代码和个人笔记。

## 环境要求

- Python 3.x

## 使用方式

各 `.py` 文件可直接运行：

```bash
python 文件名.py
```

## 目录结构

```
learning/Python/liaoxuefeng/
├── README.md          # 本说明文件
├── 5.basic/           # Python 基础
│   ├── 5.1_data-types.py      # 数据类型
│   ├── 5.2_string-encoding.py # 字符串与编码
│   ├── 5.3_list-tuple.py      # list 和 tuple
│   ├── 5.4_if.py              # 条件判断
│   ├── 5.5_match.py           # match 模式匹配
│   ├── 5.6_loop.py            # 循环
│   └── 5.7_dict-set.py        # dict 和 set
├── 6.function/        # 函数
│   ├── 6.1_call-function.py   # 调用函数（hex）
│   ├── 6.2_define-function.py # 定义函数（my_abs、quadratic）
│   ├── 6.3_parameter.py       # 函数参数（可变参数 *args）
│   └── 6.4_recursive-function.py # 递归函数（汉诺塔）
└── 7.advanced/        # 高级特性
    ├── 7.1_slice.py           # 切片（trim）
    ├── 7.2_iterate.py         # 迭代（findMinAndMax）
    └── 7.3_list-comprehension.py # 列表生成式（isinstance 过滤）
```

## 章节进度

| 章节 | 文件 | 说明 |
|------|------|------|
| 5.1 | `5.basic/5.1_data-types.py` | 数据类型——整数、浮点数、字符串（转义字符、原始字符串、多行字符串） |
| 5.2 | `5.basic/5.2_string-encoding.py` | 字符串格式化——`%` 占位符、f-string、`format()` 方法 |
| 5.3 | `5.basic/5.3_list-tuple.py` | list 嵌套与索引、tuple 不可变性 |
| 5.4 | `5.basic/5.4_if.py` | BMI 指数计算——`if`/`elif`/`else` 条件判断 |
| 5.5 | `5.basic/5.5_match.py` | `match...case` 模式匹配（守卫条件、多值匹配、默认匹配） |
| 5.6 | `5.basic/5.6_loop.py` | `for` 循环遍历 list |
| 5.7 | `5.basic/5.7_dict-set.py` | dict 的 key 限制——不可变对象 vs 含可变类型的 tuple |
| 6.1 | `6.function/6.1_call-function.py` | 调用函数——`hex()` 十六进制转换 |
| 6.2 | `6.function/6.2_define-function.py` | 定义函数——`my_abs`、`quadratic` 一元二次方程 |
| 6.3 | `6.function/6.3_parameter.py` | 函数参数——可变参数 `*args`、`mul` 乘积函数 |
| 6.4 | `6.function/6.4_recursive-function.py` | 递归函数——汉诺塔移动 |
| 7.1 | `7.advanced/7.1_slice.py` | 切片——`trim` 去除字符串首尾空格 |
| 7.2 | `7.advanced/7.2_iterate.py` | 迭代——`findMinAndMax` 查找最小最大值 |
| 7.3 | `7.advanced/7.3_list-comprehension.py` | 列表生成式——`isinstance` 类型过滤 + `.lower()` |

---

*本目录持续更新中...*

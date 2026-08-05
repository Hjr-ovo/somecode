# -*- coding: utf-8 -*-
"""
基金搜索器
==========
按关键词或代码搜索基金，输出基础信息。

用法:
    python search_fund.py <关键词或基金代码>
    python search_fund.py 摩根瑞享
    python search_fund.py 016211
"""
import sys

from eastmoney_api import search_fund


def main(keyword):
    results = search_fund(keyword)
    if not results:
        print(f"未找到与“{keyword}”相关的基金。")
        return

    print("-" * 90)
    print(f"共找到 {len(results)} 条结果，关键词：{keyword}")
    print("-" * 90)
    print(
        f"{'代码':<8}{'名称':<24}{'类型':<14}"
        f"{'最新净值':<10}{'净值日期':<12}{'基金公司':<12}{'经理'}"
    )
    print("-" * 90)
    for r in results:
        print(
            f"{r.get('FCODE',''):<8}"
            f"{r.get('SHORTNAME',''):<24}"
            f"{r.get('FTYPE',''):<14}"
            f"{r.get('DWJZ',''):<10}"
            f"{r.get('FSRQ',''):<12}"
            f"{r.get('JJGS',''):<12}"
            f"{r.get('JJJL','')}"
        )
    print("-" * 90)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
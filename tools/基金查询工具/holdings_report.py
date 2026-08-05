# -*- coding: utf-8 -*-
"""
持仓收益报告
============
查询持仓基金的当前净值，并计算每只基金的市值、收益与收益率。

用法:
    python holdings_report.py
    python holdings_report.py --config holdings.json

说明:
    - 默认读取同目录下的 holdings.json 配置（若存在），否则使用内置示例持仓。
    - 持仓配置格式（JSON）:
        {
          "110022": {"name": "易方达消费行业股票", "cost": 1000, "buy_nav": 3.5},
          "003358": {"name": "易方达中债7-10年国开行债券A", "cost": 1000, "buy_nav": 1.1}
        }
      - code: 6 位基金代码
      - name: 基金名称（仅用于展示）
      - cost: 买入金额（元）
      - buy_nav: 买入时的确认净值；若不填则无法计算收益，按成本价计入市值
"""
import argparse
import json
import os
import sys

from eastmoney_api import search_fund

# 内置示例持仓（可在 holdings.json 中覆盖，或使用 --config 指定你自己的持仓文件）
# 注意：以下为公开示例基金，非任何个人的真实持仓
DEFAULT_HOLDINGS = {
    "110022": {"name": "易方达消费行业股票", "cost": 1000, "buy_nav": 3.5},
    "161725": {"name": "招商中证白酒指数（LOF）A", "cost": 1000, "buy_nav": 0.8},
    "110011": {"name": "易方达优质精选混合（QDII）", "cost": 1000, "buy_nav": 5.0},
    "003358": {"name": "易方达中债7-10年国开行债券A", "cost": 1000, "buy_nav": 1.1},
}


def load_config(path):
    """加载持仓配置 JSON 文件"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_nav(code):
    """通过基金搜索接口获取最新净值与净值日期"""
    try:
        results = search_fund(code)
        if results:
            info = results[0]
            return info.get("DWJZ"), info.get("FSRQ")
    except Exception as e:
        return None, str(e)
    return None, "未找到"


def main():
    parser = argparse.ArgumentParser(description="持仓收益报告")
    parser.add_argument(
        "--config",
        default=None,
        help="持仓配置 JSON 文件路径；缺省时优先读 holdings.json，否则用内置示例",
    )
    args = parser.parse_args()

    holdings = None
    if args.config:
        holdings = load_config(args.config)
    else:
        default_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "holdings.json")
        if os.path.exists(default_cfg):
            holdings = load_config(default_cfg)

    if holdings is None:
        print("未找到 holdings.json，使用内置示例持仓。")
        holdings = DEFAULT_HOLDINGS

    print("=" * 78)
    print(
        f"{'基金名称':<28}{'买入':<7}{'当前净值':<10}"
        f"{'净值日期':<12}{'市值':<9}{'收益':<9}{'收益率'}"
    )
    print("=" * 78)

    total_cost = 0.0
    total_value = 0.0

    for code, item in holdings.items():
        name = item.get("name", code)
        cost = float(item.get("cost", 0))
        buy_nav = item.get("buy_nav")
        total_cost += cost

        nav, date = get_nav(code)
        if nav is None:
            print(f"{name:<28}{cost:<7.0f}{'待确认':<10}{'':<12}{'—':<9}{'—':<9}{'—'}")
            total_value += cost
            continue

        nav = float(nav)
        if buy_nav:
            shares = cost / float(buy_nav)
            value = shares * nav
            profit = value - cost
            rate = profit / cost * 100
            total_value += value
            print(
                f"{name:<28}{cost:<7.0f}{nav:<10.4f}{date:<12}"
                f"{value:<9.2f}{profit:<+9.2f}{rate:+.2f}%"
            )
        else:
            # 无买入净值，按成本计入
            total_value += cost
            print(
                f"{name:<28}{cost:<7.0f}{nav:<10.4f}{date:<12}"
                f"{'(待确认)':<9}{'—':<9}{'—'}"
            )

    print("=" * 78)
    print(f"总投入: {total_cost:.0f} 元    当前估算市值: {total_value:.2f} 元")
    if total_cost > 0:
        print(
            f"估算总收益: {total_value - total_cost:+.2f} 元    "
            f"({(total_value - total_cost) / total_cost * 100:+.2f}%)"
        )
    print("注：无买入净值（待确认）的基金按成本计入，实际收益以基金销售平台为准。")


if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
基金综合分析器
==============
输入基金代码，输出一份结构化分析报告，包含：
- 基本信息（名称/代码/成立日期/基金公司）
- 净值走势（近 N 个交易日）
- 阶段涨幅（近1月/3月/6月/1年）
- 累计净值走势
- 基金规模变动
- 基金经理信息
- 资产配置（股票/债券/现金占比）
- 持有人结构（机构/个人占比）
- 费率信息（管理/托管/销售服务/申赎费率）
- 业绩比较基准

用法:
    python fund_profiler.py <6位基金代码> [--days 10]
    python fund_profiler.py 016211
    python fund_profiler.py 016211 --days 20
"""
import argparse
import datetime
import json
import re
import sys

from eastmoney_api import (
    extract_js_var,
    fetch_fee_table,
    fetch_profile_page,
    get_fund_data,
    search_fund,
)


def _ts2date(ts, fmt="%Y-%m-%d"):
    return datetime.datetime.fromtimestamp(ts / 1000).strftime(fmt)


def parse_json(var):
    """把 JS 变量内容解析为 Python 对象"""
    if var is None:
        return None
    try:
        return json.loads(var)
    except json.JSONDecodeError:
        return var


def get_basic_info(code):
    """通过搜索接口获取基本信息，找不到时返回 None"""
    try:
        results = search_fund(code)
        return results[0] if results else None
    except Exception:
        return None


def report(code, days=10):
    content = get_fund_data(code)

    def var(name):
        return parse_json(extract_js_var(content, name))

    info = get_basic_info(code)
    lines = []

    # ---------- 基本信息 ----------
    lines.append("=" * 72)
    lines.append(f"基金综合分析报告：{info.get('SHORTNAME', code) if info else code}")
    lines.append("=" * 72)
    lines.append("【基本信息】")
    if info:
        lines.append(f"  代码: {info.get('FCODE')}    类型: {info.get('FTYPE')}")
        lines.append(f"  基金公司: {info.get('JJGS')}")
        lines.append(f"  基金经理: {info.get('JJJL')}")
        lines.append(f"  最新净值: {info.get('DWJZ')}（{info.get('FSRQ')}）")
        lines.append(f"  最低申购: {info.get('MINSG')} 元")
    lines.append(f"  业绩基准: {_profile_field('业绩比较基准')}")

    # ---------- 阶段涨幅 ----------
    lines.append("\n【阶段涨幅】")
    syl_fields = [
        ("syl_1y", "近1月"),
        ("syl_3y", "近3月"),
        ("syl_6y", "近6月"),
        ("syl_1n", "近1年"),
    ]
    for js_var, label in syl_fields:
        m = re.search(r'var\s+' + js_var + r'\s*=\s*"([^"]*)"', content)
        value = m.group(1) if m else "N/A"
        lines.append(f"  {label}: {value}%")

    # ---------- 净值走势 ----------
    trend = var("Data_netWorthTrend")
    lines.append(f"\n【净值走势 · 近{days}个交易日】")
    if trend:
        for item in trend[-days:]:
            d = _ts2date(item["x"])
            er = item.get("equityReturn")
            lines.append(f"  {d}  净值 {item['y']}  日涨跌 {er}%")
    else:
        lines.append("  暂无数据")

    # ---------- 累计净值 ----------
    ac = var("Data_ACWorthTrend")
    if ac:
        lines.append("\n【累计净值 · 最近5期】")
        for item in ac[-5:]:
            lines.append(f"  {_ts2date(item[0])}  累计净值 {item[1]}")

    # ---------- 规模变动 ----------
    scale = var("Data_fluctuationScale")
    if scale:
        cats = scale.get("categories", [])
        series = scale.get("series", [])
        # series 是列表，每个元素对应一个日期，y 为规模值
        ys = [s.get("y") for s in series] if series else []
        lines.append(f"\n【规模变动 · 最近{len(cats)}期】")
        for c, y in zip(cats, ys):
            lines.append(f"  {c}  规模 {y} 亿元")
    else:
        lines.append("\n【规模变动】暂无数据")

    # ---------- 基金经理 ----------
    managers = var("Data_currentFundManager")
    if managers:
        lines.append("\n【基金经理】")
        for mgr in managers:
            lines.append(f"  姓名: {mgr.get('name')}  从业: {mgr.get('workTime')}")
            lines.append(f"  管理规模: {mgr.get('fundSize')}")
            lines.append(f"  简介: {mgr.get('desc', 'N/A')[:120]}")

    # ---------- 资产配置 ----------
    alloc = var("Data_assetAllocation")
    if alloc:
        lines.append("\n【资产配置 · 最近3期】")
        cats = alloc.get("categories", [])
        series = {s["name"]: s["data"] for s in alloc.get("series", [])}
        for i, c in enumerate(cats[-3:], start=len(cats) - 3):
            pass
        for i in range(max(0, len(cats) - 3), len(cats)):
            bond = series.get("债券占净比", [])
            stock = series.get("股票占净比", [])
            cash = series.get("现金占净比", [])
            bond_v = bond[i] if i < len(bond) else 0
            stock_v = stock[i] if i < len(stock) else 0
            cash_v = cash[i] if i < len(cash) else 0
            lines.append(
                f"  {cats[i]}  股票 {stock_v:.2f}%  债券 {bond_v:.2f}%  现金 {cash_v:.2f}%"
            )

    # ---------- 持有人结构 ----------
    holder = var("Data_holderStructure")
    if holder:
        lines.append("\n【持有人结构 · 最近2期】")
        cats = holder.get("categories", [])
        series = {s["name"]: s["data"] for s in holder.get("series", [])}
        for i in range(max(0, len(cats) - 2), len(cats)):
            org = series.get("机构持有比例", [])
            per = series.get("个人持有比例", [])
            org_v = org[i] if i < len(org) else 0
            per_v = per[i] if i < len(per) else 0
            lines.append(
                f"  {cats[i]}  机构 {org_v:.2f}%  个人 {per_v:.2f}%"
            )

    # ---------- 费率 ----------
    lines.append("\n【费率信息】")
    fee_html = fetch_fee_table(code)
    # HTML 结构: 管理费率</td><td class="w135">0.30%（每年）</td>
    for label in ["管理费率", "托管费率", "销售服务费率"]:
        idx = fee_html.find(label)
        if idx >= 0:
            snippet = fee_html[idx:idx + 120]
            m = re.search(r"</td><td[^>]*>([\d.]+)%", snippet)
            if m:
                lines.append(f"  {label}: {m.group(1)}%/年")
    # 申赎费
    for label in ["申购费率", "赎回费率"]:
        idx = fee_html.find(label)
        if idx >= 0:
            snippet = fee_html[idx:idx + 250]
            m = re.search(
                r"<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>"
                r"\s*<td[^>]*>([^<]+)</td>",
                snippet,
            )
            if m:
                lines.append(f"  {label}: {m.group(1).strip()} / {m.group(2).strip()} / {m.group(3).strip()}")

    lines.append("\n" + "=" * 72)
    print("\n".join(lines))


def _profile_field(label):
    """从档案页提取指定字段的值"""
    try:
        html = fetch_profile_page(code)
        idx = html.find(label)
        if idx >= 0:
            snippet = html[idx:idx + 400]
            m = re.search(r"<td[^>]*>\s*(.*?)\s*</td>", snippet, re.S)
            if m:
                return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    except Exception:
        pass
    return "N/A"


def main():
    global code
    parser = argparse.ArgumentParser(description="基金综合分析器")
    parser.add_argument("code", help="6 位基金代码，如 016211")
    parser.add_argument("--days", type=int, default=10, help="展示近 N 个交易日（默认10）")
    args = parser.parse_args()
    code = args.code
    if not re.fullmatch(r"\d{6}", args.code):
        print("错误：基金代码应为 6 位数字。")
        sys.exit(1)
    report(args.code, args.days)


if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
东方财富公开基金数据接口封装（仅供学习研究使用）
=================================================

从东方财富（eastmoney）公开网页接口获取基金数据，无第三方依赖，仅使用 Python 标准库。

提供的函数：
- search_fund(keyword)      : 按基金名称或代码搜索，返回基础信息列表
- get_fund_data(code)       : 获取基金核心数据（净值/规模/经理等，原始 JS 字符串）
- extract_js_var(content, name) : 从核心数据 JS 中提取指定变量的原始内容
- fetch_fee_table(code)     : 获取基金费率页面 HTML
- fetch_profile_page(code)  : 获取基金档案页面 HTML
"""
import json
import re
import urllib.parse
import urllib.request

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}

SEARCH_API = (
    "https://fundsuggest.eastmoney.com/FundSearch/api/"
    "FundSearchAPI.ashx?m=1&key={keyword}"
)
PINGZHONG_API = "https://fund.eastmoney.com/pingzhongdata/{code}.js?v={code}"
FEE_API = "https://fundf10.eastmoney.com/jjfl_{code}.html"
PROFILE_API = "https://fundf10.eastmoney.com/jbgk_{code}.html"


def http_get(url, timeout=15):
    """请求 URL 并返回原始字节内容"""
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def search_fund(keyword):
    """
    按名称或代码搜索基金。

    参数:
        keyword: 基金名称关键词或基金代码，如 "摩根瑞享" 或 "016211"

    返回:
        基金基础信息字典列表，每个字典包含 FCODE / SHORTNAME / FTYPE /
        DWJZ / FSRQ / JJGS / JJJL 等字段。
    """
    url = SEARCH_API.format(keyword=urllib.parse.quote(keyword))
    data = json.loads(http_get(url).decode("utf-8"))
    return [d["FundBaseInfo"] for d in data.get("Datas", [])]


def get_fund_data(code):
    """
    获取基金核心数据文件（pingzhongdata.js）。

    该文件是单个 JS 表达式文本，其中包含以下常用变量：
        Data_netWorthTrend      单位净值走势
        Data_ACWorthTrend       累计净值走势
        Data_fluctuationScale   规模变动
        Data_currentFundManager 现任基金经理
        Data_assetAllocation    资产配置（股债现金占比）
        Data_holderStructure    持有人结构
        Data_grandTotal         阶段收益累计曲线
        syl_1n / syl_6y / syl_3y / syl_1y  近1年/6月/3月/1月涨幅
        fund_sourceRate         原费率
        fS_name / fS_code       基金名称 / 代码

    参数:
        code: 6 位基金代码，如 "016211"

    返回:
        单个 JS 表达式字符串（UTF-8 无 BOM）。
    """
    return http_get(PINGZHONG_API.format(code=code)).decode("utf-8-sig")


def extract_js_var(content, name):
    """
    从 get_fund_data() 返回的 JS 文本中提取 var name = ...; 的原始内容。

    参数:
        content: get_fund_data() 返回的 JS 字符串
        name:    变量名，如 "Data_netWorthTrend"

    返回:
        变量值字符串；未找到返回 None。
    """
    m = re.search(r"var\s+" + re.escape(name) + r"\s*=(.*?);", content, re.S)
    return m.group(1).strip() if m else None


def fetch_fee_table(code):
    """获取基金费率页面 HTML（管理费/托管费/销售服务费/申赎费率）"""
    return http_get(FEE_API.format(code=code)).decode("utf-8")


def fetch_profile_page(code):
    """获取基金档案页面 HTML（成立日期/类型/规模/业绩基准等）"""
    return http_get(PROFILE_API.format(code=code)).decode("utf-8")


if __name__ == "__main__":
    # 自测：搜索基金代码
    for item in search_fund("摩根瑞享"):
        print(item["FCODE"], item["SHORTNAME"], item["FTYPE"], item["DWJZ"])
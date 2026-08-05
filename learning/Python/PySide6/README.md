# 🐍 Python Qt 学习项目

> 本目录用于记录 PySide6（Qt for Python）桌面应用开发的学习过程。

## 简介

这是我学习 Python Qt 桌面应用开发的练习项目合集，使用 **PySide6**（Qt 的官方 Python 绑定）进行开发。每个文件是一个独立的练习程序，从基础到进阶逐步实践，**文件名前的数字代表学习顺序**。

📖 课程来源：[https://www.byhy.net/](https://www.byhy.net/)

## 环境要求

- Python 3.8+
- PySide6

```bash
pip install PySide6
```

## 文件列表

| # | 文件 | 说明 | 分类 |
|---|------|------|------|
| 01 | `01_salary_ui.py` | 薪资统计工具——界面布局，按钮和文本编辑框基本用法 | 薪资统计 |
| 02 | `02_salary_func.py` | 在 01 基础上实现统计按钮功能，按薪资 20000 划分显示人员名单 | 薪资统计 |
| 03 | `03_salary_class.py` | 在 02 基础上使用类封装界面和功能，提升代码组织性 | 薪资统计 |
| 04 | `04_salary_ui_loader.py` | 使用 Qt Designer UI 文件加载界面，实现界面与逻辑分离 | 薪资统计 |
| 05 | `05_http_client_tool.py` | HTTP 接口测试工具，支持 GET/POST/PUT/DELETE，可自定义请求头和请求体 | HTTP 工具 |
| 06 | `06_painter_basic.py` | QPainter 绘图基础——自定义 QWidget 绘制线条，展示画笔使用 | 绘图 |
| 07 | `07_painter_pen.py` | QPainter 画笔——设置画笔颜色和宽度绘制线条 | 绘图 |
| 08 | `08_painter_point.py` | QPainter 画点——使用画笔绘制点 | 绘图 |
| 09 | `09_painter_rect.py` | QPainter 画矩形——绘制矩形图形 | 绘图 |
| 10 | `10_painter_ellipse.py` | QPainter 画椭圆——绘制矩形和椭圆对比 | 绘图 |
| 11 | `11_painter_brush.py` | QPainter 画刷——使用 QBrush 设置填充样式 | 绘图 |
| 12 | `12_painter_text.py` | QPainter 绘制文字——设置字体、颜色绘制文本 | 绘图 |
| 13 | `13_painter_custom_widget.py` | QPainter 自定义控件——绘制插座图形，展示控件复用 | 绘图 |
| | | |
| | `ui/` | 存放 Qt Designer 生成的 `.ui` 界面文件 |
| | `dist/` | 存放打包后的 exe 可执行文件（`05_http_client_tool.exe`） |

### 05_http_client_tool.py 补充说明

- **功能**：图形化 HTTP 请求调试工具，可自由添加/删除请求头，发送请求并查看响应
- **开发运行**：`python 05_http_client_tool.py`
- **exe 打包**：使用 PyInstaller 打包，exe 位于 `dist/05_http_client_tool.exe`，**无需额外依赖**，双击即可运行
- **打包命令**：
  ```bash
  python -m PyInstaller --distpath "dist" --workpath "build" --add-data "ui/5.ui;." --onefile --windowed 05_http_client_tool.py
  ```
- **注意事项**：需配合 `ui/5.ui` 界面文件使用，若修改了 `5.ui` 需重新打包才会生效


## 运行方式

```bash
cd learning/Python/PySide6
python 文件名.py
```

例如：

```bash
python 01_salary_ui.py
```

---

*本目录持续更新中...*
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
import requests, traceback, os, sys
from PySide6.QtGui import  QIcon

# 获取资源文件路径（兼容 .py 开发环境和 PyInstaller 打包后的 exe）
def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller 打包后，资源文件会被解压到 sys._MEIPASS 临时目录
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境下，使用当前脚本文件所在的目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# 在QApplication之前先实例化
uiLoader = QUiLoader()

class HttpTest:

    def __init__(self):
        # 再加载界面
        # 原方案（仅开发环境可用）：
        # self.ui = uiLoader.load('python Qt/ui/5.ui')
        # 新方案（兼容开发环境和打包后的 exe）：
        self.ui = uiLoader.load(resource_path('ui/5.ui'))

        self.ui.resize(900,700)
        self.ui.box_method.addItems(['GET', 'POST', 'PUT', 'DELETE' ])

        self.ui.table_http_headers.horizontalHeader().setStretchLastSection(True)
        self.ui.table_http_headers.setColumnWidth(0, 180)

        self.ui.btn_add_header.clicked.connect(self.addOneHeader)
        self.ui.btn_del_header.clicked.connect(self.delOneHeader)

        self.ui.btn_send.clicked.connect(self.sendRequest)

        self.ui.btn_clear.clicked.connect(self.ui.output_window.clear)

    def addOneHeader(self):
        rowNo = self.ui.table_http_headers.currentRow() + 1
        self.ui.table_http_headers.insertRow(rowNo)

    def delOneHeader(self):
        self.ui.table_http_headers.removeRow(
            self.ui.table_http_headers.currentRow()
        )

    def sendRequest(self):
        method = self.ui.box_method.currentText()
        url    = self.ui.edit_url.text()
        payload = self.ui.edit_body.toPlainText()

        # 获取消息头
        headers = {}
        ht = self.ui.table_http_headers
        for row in range(ht.rowCount()):
            k = ht.item(row,0).text()
            v = ht.item(row,1).text()
            if k.strip() == '':
                continue
            headers[k] = v

        req = requests.Request(method,url=url,headers=headers,data=payload)
        prepared = req.prepare()
        self.pretty_print_request(prepared)

        s = requests.Session()

        try:
            res = s.send(prepared)
            self.ui.output_window.append(
                '\n\n----------- 得到响应 -----------\nHTTP/1.1 {}\n{}\n\n{}'.format(
                    res.status_code,
                    '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                    res.text,
                ))
        except:
            self.ui.output_window.append(
                traceback.format_exc())


    def pretty_print_request(self,req):

        if req.body == None:
            msgBody = ''
        else:
            msgBody = req.body

        self.ui.output_window.append(
            '{}\n{}\n{}\n\n{}'.format(
            '\n\n----------- 发送请求 -----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            msgBody,
        ))


app = QApplication([])
# 加载 icon
app.setWindowIcon(QIcon(resource_path('assets/logo.ico')))
stats = HttpTest()
stats.ui.show()
app.exec() # PySide6 是 exec 而不是 exec_
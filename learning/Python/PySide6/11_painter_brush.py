from PySide6 import  QtGui, QtWidgets 
from PySide6.QtCore import Qt

class MyWidget(QtWidgets.QWidget):

    def paintEvent(self, e): 
        painter = QtGui.QPainter(self)

        # 创建画刷QBrush对象
        brush = QtGui.QBrush()
        # 设置画刷的颜色
        brush.setColor(QtGui.QColor("yellow"))
        # 设置画刷的填充样式
        brush.setStyle(Qt.SolidPattern)

        # 指定使用这个画刷对象
        painter.setBrush(brush)

        # 画图
        painter.drawRect(50, 50, 100,100)        
        painter.drawEllipse(200, 200, 100,100)

        painter.end() 
       
       
app = QtWidgets.QApplication()

window = QtWidgets.QMainWindow()
window.resize(500, 500)

my = MyWidget(window)
my.resize(500,500)

window.show()
app.exec()
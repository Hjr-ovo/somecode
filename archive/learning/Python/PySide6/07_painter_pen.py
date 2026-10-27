from PySide6 import  QtGui, QtWidgets 
 
class MyWidget(QtWidgets.QWidget):

    def paintEvent(self, e):
        painter = QtGui.QPainter(self) 

        # 创建画笔对象
        pen = QtGui.QPen()
        pen.setWidth(3) # 宽度为3个像素
        pen.setColor(QtGui.QColor('red')) #颜色为红色

        # 设置 painter 的画笔属性对象
        painter.setPen(pen)

        painter.drawLine(50, 80, 200, 300)
        painter.end()

app = QtWidgets.QApplication()
window = QtWidgets.QMainWindow()
window.resize(500, 500)
 
my = MyWidget(window)
my.resize(500,500)
 
window.show()
app.exec()
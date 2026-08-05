from PySide6 import  QtGui, QtWidgets 

class MyWidget(QtWidgets.QWidget):

    def paintEvent(self, e): 
        painter = QtGui.QPainter(self)

        # 创建画笔对象
        pen = QtGui.QPen()
        pen.setWidth(10) # 宽度为10个像素
        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)

        # 画一个点坐标为 200, 150
        painter.drawPoint(200, 150)
        
        painter.end()

app = QtWidgets.QApplication()
window = QtWidgets.QMainWindow()
window.resize(500, 500)
 
my = MyWidget(window)
my.resize(500,500)
 
window.show()
app.exec()        
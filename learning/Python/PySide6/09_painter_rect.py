from PySide6 import  QtGui, QtWidgets 

class MyWidget(QtWidgets.QWidget):

    def paintEvent(self, e): 
        painter = QtGui.QPainter(self)

        # 画一个矩形，左上角坐标为 50, 50
        # 宽度为200像素，高度为100像素
        painter.drawRect(50, 50, 300,300)
        
        painter.end()

app = QtWidgets.QApplication()
window = QtWidgets.QMainWindow()
window.resize(500, 500)
 
my = MyWidget(window)
my.resize(500,500)
 
window.show()
app.exec()        
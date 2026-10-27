from PySide6 import  QtGui, QtWidgets 

class MyWidget(QtWidgets.QWidget):

    def paintEvent(self, e): 
        painter = QtGui.QPainter(self)
        # 防锯齿
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.drawRect(50, 50, 300,200)
        
        # 画一个椭圆，左上角坐标为 50, 50
        # 水平方向直径为300像素，垂直方向直径为200像素
        painter.drawEllipse(50, 50, 300,200)
        painter.end()

app = QtWidgets.QApplication()
window = QtWidgets.QMainWindow()
window.resize(500, 500)
 
my = MyWidget(window)
my.resize(500,500)
 
window.show()
app.exec()        
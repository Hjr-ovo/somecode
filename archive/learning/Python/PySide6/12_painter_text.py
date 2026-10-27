from PySide6 import  QtGui, QtWidgets 

class MyWidget(QtWidgets.QWidget):

    def paintEvent(self, e): 
        painter = QtGui.QPainter(self)

        # 文字的粗细颜色，由画笔属性决定
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen) # 设置画笔

        # 字体
        font = QtGui.QFont()
        font.setFamily('黑体') #字体类型
        font.setPointSize(30)  # 字体大小
        painter.setFont(font)  # 设置字体

        painter.drawText(100, 100, 'hello，然然然!')

        painter.end() 
       
       
app = QtWidgets.QApplication()

window = QtWidgets.QMainWindow()
window.resize(500, 500)

my = MyWidget(window)
my.resize(500,500)

window.show()
app.exec()
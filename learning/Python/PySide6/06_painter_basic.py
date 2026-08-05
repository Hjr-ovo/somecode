from PySide6 import  QtGui, QtWidgets 

# 自定义一个QWidget的子类
class MyWidget(QtWidgets.QWidget):
 
    # QWidget类的 paintEvent方法会被Qt调用画出控件自身的形象
    def paintEvent(self, e): 
        # 参数 是绘制图形 目标对象
        painter = QtGui.QPainter(self)  
 
        # 防锯齿
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # 画一条线，起点坐标为 50,80 ; 终点坐标为 200,300
        painter.drawLine(50, 80, 200, 300)  
        
        painter.end() # 结束绘制
       
app = QtWidgets.QApplication()
window = QtWidgets.QMainWindow()
window.resize(500, 500)
 
my = MyWidget(window)
my.resize(500,500)
 
window.show()
app.exec()
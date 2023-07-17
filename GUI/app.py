import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from .views import Window

def main():
    # 创建Applicants
    app = QApplication(sys.argv)
    # 创建主窗口
    win = Window()
    # 设置应用程序图标
    icon = QIcon('./resources/icon.png')
    app.instance().setWindowIcon(icon)
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    win.show()
    # 设置结束
    sys.exit(app.exec())
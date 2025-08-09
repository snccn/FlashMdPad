import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import ( QColor, QPalette, QIcon, QAction)
from PySide6.QtWidgets import (QApplication,QMenu, QSystemTrayIcon)

from app.ui import MarkdownEditor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 设置应用样式
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon("icon.png"))


    # 设置调色板
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    editor = MarkdownEditor()
    editor.show()


    tray = QSystemTrayIcon()
    tray.setIcon(QIcon("./icon.png"))
    tray.setVisible(True)

    @Slot()
    def show_app():
        editor.show()

    menu = QMenu()
    action = QAction('打开主窗口')
    action.triggered.connect(show_app)
    menu.addAction(action)

    tray_quit = QAction('退出')
    tray_quit.triggered.connect(app.quit)
    menu.addAction(tray_quit)

    tray.setContextMenu(menu)

    sys.exit(app.exec())
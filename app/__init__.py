# coding:utf-8
import sys
import os

from PySide6.QtCore import Slot
from PySide6.QtGui import ( QColor, QPalette, QIcon, QAction, QKeySequence)
from PySide6.QtWidgets import (QApplication,QMenu, QSystemTrayIcon)

from app.ui import MarkdownEditor


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstaller 临时解压路径
else:
    base_path = os.path.realpath(".")

# 设置应用样式
if sys.platform == "darwin":
    APPSTYLE = "fusion"
    TRAY_MODE = False
    icon_resource_path = os.path.join(base_path, 'resources/icons/icon.png')
elif sys.platform == "win32":
    icon_resource_path = os.path.join(base_path, 'resources/icons/icon.png')
    try:
        APPSTYLE = "windowsvista"
        TRAY_MODE = True
    except:
        APPSTYLE = "fusion"
        TRAY_MODE = True
else:
    APPSTYLE = "fusion"
    TRAY_MODE = True


def CreateApp(argv:list[str]=sys.argv):
    app = QApplication(argv)
    
    app.setQuitOnLastWindowClosed(TRAY_MODE)
    
    app.setWindowIcon(QIcon(icon_resource_path))
    app.setStyle(APPSTYLE)

    # 设置调色板
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    editor = MarkdownEditor()
    editor.show()

    if not sys.platform == "darwin":
        tray = QSystemTrayIcon()
        tray.setToolTip("FlashMdPad")
        tray.setIcon(QIcon(icon_resource_path))
        tray.setVisible(True)

        @Slot()
        def show_app():
            editor.show()

        @Slot()
        def hide_and_show_app(reason):
            if reason == QSystemTrayIcon.Trigger:  # 左键单击
                editor.hide_and_show()


        menu = QMenu()
        action = QAction('打开主窗口')
        action.triggered.connect(show_app)
        menu.addAction(action)

        tray_quit = QAction('退出')
        tray_quit.triggered.connect(app.quit)
        menu.addAction(tray_quit)

        tray.setContextMenu(menu)
        tray.activated.connect(hide_and_show_app)

    sys.exit(app.exec())
    return app
    pass


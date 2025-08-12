# coding:utf-8

import os
from PySide6.QtGui import (Qt, QAction, QIcon, QKeySequence, QPalette,QColor,QTextCursor)
from PySide6.QtWidgets import (QMainWindow, QTabWidget, QWidget,QInputDialog,
                              QVBoxLayout,QApplication,QPushButton,QToolBar,QFontDialog,
                              QLabel, QFileDialog, QMessageBox, QStatusBar)
from PySide6.QtCore import QSize,Signal,QSettings

from app.utils import MarkdownTab
from app.filemanager import FileManager, rename_with_pathlib
from app.dialogs import FindDialog
import time
import datetime

class MarkdownEditor(QMainWindow):
    """主窗口：多标签Markdown编辑器"""
    themeChanged = Signal(bool)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlashMdPad")
        self.resize(1200, 800)
        self.setup_ui()
        self.setup_menu()
        # self.setup_toolbar()
        self.setup_statusbar()
        self.dark_mode = False
        self.fm = FileManager()
        self.font = ""

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground, False)
        
        # 初始标签页
        if len(self.fm.FileList) == 0:
            self.add_new_tab()
        else:
            for i in self.fm.FileList:
                self.add_new_tab(i)

        self.themeChanged.connect(self.update_theme)
    
    def setup_ui(self):
        # 主中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_status)
        
        main_layout.addWidget(self.tab_widget)
    
    def setup_menu(self):
        # 文件菜单
        file_menu = self.menuBar().addMenu("文件")
        
        # 新建
        new_action = QAction(QIcon.fromTheme("document-new"), "新建", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_action)
        
        # # 从文件中导入
        # open_action = QAction(QIcon.fromTheme("document-open"), "从文件中导入", self)
        # open_action.setShortcut(QKeySequence("Ctrl+I"))
        # open_action.triggered.connect(self.open_file)
        # file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # 保存
        save_action = QAction(QIcon.fromTheme("document-save"), "保存", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_current)
        file_menu.addAction(save_action)
        
        # 另存为
        save_as_action = QAction("另存为...", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_as_current)
        file_menu.addAction(save_as_action)
        
        # 重命名
        rename_action = QAction("重命名", self)
        rename_action.setShortcut(QKeySequence("Ctrl+U"))
        rename_action.triggered.connect(self.rename)
        file_menu.addAction(rename_action)

        file_menu.addSeparator()

        hide_action = QAction("隐藏窗口",self)
        hide_action.setShortcut(QKeySequence("ESC"))
        hide_action.triggered.connect(self.hide)
        file_menu.addAction(hide_action)
        
        # 退出
        exit_action = QAction("退出", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = self.menuBar().addMenu("编辑")
        
        # 撤销
        undo_action = QAction("撤销", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        # 重做
        redo_action = QAction("重做", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # 查找
        find_action = QAction("查找", self)
        find_action.setShortcut(QKeySequence.Find)
        find_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(find_action)
        
        # 视图菜单
        view_menu = self.menuBar().addMenu("视图")
        
        # 深色模式
        self.dark_mode_action = QAction("深色模式", self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        # view_menu.addAction(self.dark_mode_action)

        # 字体设置
        self.set_font_action = QAction("字体设置", self)
        self.set_font_action.triggered.connect(self.SetFontFamily)
        view_menu.addAction(self.set_font_action)
        
        # 窗口保持在顶层
        self.set_ontop_action = QAction("窗口保持在顶层", self)
        self.set_ontop_action.setCheckable(True)
        self.set_ontop_action.setShortcut(QKeySequence("F6"))
        self.set_ontop_action.triggered.connect(lambda checked: self.set_window_on_top(checked))
        view_menu.addAction(self.set_ontop_action)

        # 标签页菜单
        tab_menu = self.menuBar().addMenu("标签页")
        
        # 新建标签页
        new_tab_action = QAction("新建标签页", self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(self.add_new_tab)
        tab_menu.addAction(new_tab_action)
        
        # 关闭标签页
        close_tab_action = QAction("关闭标签页", self)
        close_tab_action.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_action.triggered.connect(self.delete_current)
        tab_menu.addAction(close_tab_action)

        # 插入工具栏
        tab_menu = self.menuBar().addMenu("插入")

        # 插入分隔符
        add_split_action = QAction("分隔行", self)
        add_split_action.setShortcut(QKeySequence("Ctrl+-"))
        add_split_action.triggered.connect(self.add_split)
        tab_menu.addAction(add_split_action)

        # 插入当前时间
        add_date_action = QAction("日期时间", self)
        add_date_action.setShortcut(QKeySequence("Ctrl+D"))
        add_date_action.triggered.connect(self.add_date)
        tab_menu.addAction(add_date_action)

        # 运算
        caculate_action = QAction("运算表达式", self)
        caculate_action.setShortcut(QKeySequence("Ctrl+E"))
        caculate_action.triggered.connect(self.caculate_current_row)
        tab_menu.addAction(caculate_action)

    def setup_toolbar(self):
        """设置工具栏"""
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        
        # 新建
        new_action = QAction("新建", self)
        new_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_action)
        
        # 保存
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_current)
        toolbar.addAction(save_action)
        
        # 删除
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self.delete_current)
        toolbar.addAction(delete_action)

        toolbar.addSeparator()
        
        # 撤销
        undo_action = QAction(QIcon.fromTheme("edit-undo"), "撤销", self)
        undo_action.triggered.connect(self.undo)
        toolbar.addAction(undo_action)
        
        # 重做
        redo_action = QAction(QIcon.fromTheme("edit-redo"), "重做", self)
        redo_action.triggered.connect(self.redo)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        
        # 深色模式切换按钮
        self.dark_mode_toggle = QPushButton("🌙 深色模式")
        self.dark_mode_toggle.setCheckable(True)
        self.dark_mode_toggle.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                border: 1px solid #cbd5e0;
                border-radius: 4px;
                background-color: #f7fafc;
            }
            QPushButton:checked {
                background-color: #2d3748;
                color: #e2e8f0;
            }
        """)
        self.dark_mode_toggle.toggled.connect(self.toggle_dark_mode)
        toolbar.addWidget(self.dark_mode_toggle)
        toolbar.addSeparator()

    def setup_statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)
        self.position_label = QLabel("行:1 列:1")
        self.status_bar.addPermanentWidget(self.position_label)
    
    def add_new_tab(self, file_path=None):
        """添加新标签页"""

        if not file_path:
            file_path = os.path.realpath(os.path.join(self.fm.path, f"newdoc_{round(time.time())}"))
        tab = MarkdownTab(self, file_path, dark_mode=self.dark_mode)
        
        # 获取标签索引
        index = self.tab_widget.addTab(tab, "新文档")
        self.tab_widget.setCurrentIndex(index)
        
        # 设置标签标题
        self.update_tab_title(tab)
        
        # 连接光标位置变化信号
        tab.editor.cursorPositionChanged.connect(self.update_cursor_position)

        # 连接修改状态变化信号
        tab.modificationChanged.connect(self.update_tab_title)

        # 创建文件时默认保存当前文件
        self.save_current()
        
        return tab
    
    def update_tab_title(self, tab):
        """更新标签标题（显示文件名和修改状态）"""
        index = self.tab_widget.indexOf(tab)
        if index == -1:
            return
            
        file_name = "新文档"
        if tab.file_path:
            file_name = os.path.basename(tab.file_path)
            
        modified = "*" if tab.is_modified else ""
        self.tab_widget.setTabText(index, f"{file_name}{modified}")
    
    def get_current_tab(self):
        """获取当前标签页"""
        return self.tab_widget.currentWidget()
    
    # def open_file(self):
    #     """打开文件"""
    #     file_path, _ = QFileDialog.getOpenFileName(
    #         self, "打开Markdown文件", 
    #         os.path.expanduser("~"), 
    #         "Markdown Files (*.md *.markdown);;All Files (*)"
    #     )
        
    #     if file_path:
    #         with open(file_path, "r", encoding="utf-8") as f:
    #             content = f.read()
    #         tab = self.get_current_tab()
    #         if tab:
    #             # 插入到当前光标处
    #             cursor = tab.editor.textCursor()
    #             cursor.insertText(content)
    
    def save_current(self):
        """保存当前文档"""
        tab = self.get_current_tab()
        if tab:
            if tab.save_file():
                self.update_tab_title(tab)
    
    def save_as_current(self):
        """当前文档另存为"""
        tab = self.get_current_tab()
        if tab:
            if tab.save_as():
                self.update_tab_title(tab)
    
    def close_current_tab(self):
        """关闭当前标签页"""
        index = self.tab_widget.currentIndex()
        if index >= 0:
            self.close_tab(index)
    
    def close_tab(self, index):
        """关闭指定标签页"""
        tab = self.tab_widget.widget(index)
        if tab and tab.is_modified:
            reply = QMessageBox.question(
                self, "未保存的更改",
                f"文档 {os.path.basename(tab.file_path) if tab.file_path else '新文档'} 有未保存的更改，是否保存?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                if not tab.save_file():
                    return  # 如果保存失败，不关闭标签页
            elif reply == QMessageBox.Cancel:
                return
        
        self.tab_widget.removeTab(index)
        tab.deleteLater()
        
        # 如果没有标签页了，创建一个新的
        if self.tab_widget.count() == 0:
            self.add_new_tab()
    
    def undo(self):
        """撤销操作"""
        tab = self.get_current_tab()
        if tab:
            tab.editor.undo()
    
    def redo(self):
        """重做操作"""
        tab = self.get_current_tab()
        if tab:
            tab.editor.redo()
    
    def update_cursor_position(self):
        """更新状态栏光标位置"""
        tab = self.get_current_tab()
        if tab:
            cursor = tab.editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.position_label.setText(f"行:{line} 列:{col}")
    
    def update_status(self, index):
        """更新状态栏信息"""
        if index >= 0:
            tab = self.tab_widget.widget(index)
            if tab.file_path:
                self.status_label.setText(f"已打开: {tab.file_path}")
            else:
                self.status_label.setText("新文档")
            self.update_cursor_position()
        else:
            self.status_label.setText("就绪")

    def toggle_dark_mode(self, checked):
        """切换深色模式"""
        self.dark_mode = checked
        self.themeChanged.emit(checked)  # 发出主题变化信号

    def update_theme(self, dark_mode):
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if tab:
                tab.toggle_dark_mode(dark_mode)
        
        # 更新主窗口样式
        if dark_mode:
            # 深色模式
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor("#1a202c"))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor("#2d3748"))
            palette.setColor(QPalette.AlternateBase, QColor("#1a202c"))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor("#2d3748"))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor("#63b3ed"))
            palette.setColor(QPalette.Highlight, QColor("#4a5568"))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            QApplication.setPalette(palette)
        else:
            # 浅色模式
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(191, 222, 255))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.setPalette(palette)
        
        # 更新菜单和工具栏状态
        # self.dark_mode_action.setChecked(dark_mode)
        # self.dark_mode_toggle.setText("☀️ 浅色模式" if dark_mode else "🌙 深色模式")
    
    def add_split(self):
        self.get_current_tab().add_str_to_editor("-------------------")

    def add_date(self):
        now = datetime.datetime.now()
        date_str = now.strftime(f"%Y-%m-%d %H:%M")
        self.get_current_tab().add_str_to_editor(f"{date_str}")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def delete_current(self):
        tab = self.get_current_tab()
        msg_box = QMessageBox(
            QMessageBox.Warning,
            "确认删除",
            f"你确定要删除当前标签页的文件\n\n{tab.file_path}" + "\n\n删除后将无法恢复！",
            QMessageBox.Yes | QMessageBox.No,
            self
        )
    
        # 可以自定义按钮文本
        msg_box.setButtonText(QMessageBox.Yes, "删除")
        msg_box.setButtonText(QMessageBox.No, "取消")
        result = msg_box.exec()
        if result == QMessageBox.Yes:
            # 移除列表中的项目（实际应用中可以在这里添加真实删除文件的代码）
            self.fm.delete_file(tab.file_path)
            self.close_current_tab()
        pass

    # 判断当前窗口是隐藏的话就显示，显示的话就隐藏
    def hide_and_show(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
        pass

    def rename(self):
        file_path = self.get_current_tab().file_path
        file_name = file_path.split(self.fm.path)[-1]
        text, ok = QInputDialog.getText(
            self,  # 父窗口
            "重命名",  # 标题
            "请输入文件名:",  # 提示文本
            text=file_name  # 默认文本
        )
        if ok and text:
            new_path = os.path.join(self.fm.path, text)
            if rename_with_pathlib(old_path=file_path, new_path= new_path):
                self.get_current_tab().file_path = new_path
                self.update_tab_title(self.get_current_tab())
        pass

    def onexit(self,event):
        """关闭窗口时检查所有标签页的未保存更改"""
        unsaved_tabs = []
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if tab.is_modified:
                name = os.path.basename(tab.file_path) if tab.file_path else "新文档"
                unsaved_tabs.append(name)
        
        if unsaved_tabs:
            tab_list = "\n".join(f"- {name}" for name in unsaved_tabs)
            reply = QMessageBox.question(
                self, "未保存的更改",
                f"以下文档有未保存的更改:\n{tab_list}\n\n是否退出?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                for i in range(self.tab_widget.count()):
                    tab = self.tab_widget.widget(i)
                    if tab.is_modified:
                        if not tab.save_file():
                            event.ignore()
                            return
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        
        event.accept()

    def set_window_on_top(self,on_top: bool):
        """设置窗口是否保持在顶层"""
        self.setWindowFlag(Qt.WindowStaysOnTopHint, on_top)
        self.hide()
        # time.sleep(1)
        self.show()  # 需要重新 show 才会生效

    def SetFontFamily(self):
        current_font = self.get_current_tab().font()
        ok, font = QFontDialog.getFont(current_font, self, "选择字体")

        if ok:
            self.get_current_tab().setFont(font)
            settings = QSettings("FlashMdPad", "UserSettings")
            settings.setValue("editorFont", font.toString())
    def show_find_dialog(self):
        dialog = FindDialog(self)
        if dialog.exec():
            text = dialog.get_text()
            self.find_in_editor(text)

    def find_in_editor(self, text):
        tab = self.get_current_tab()
        if not tab or not text:
            return
        editor = tab.editor
        # 查找下一个
        found = editor.find(text)
        if not found:
            # 没找到，从头再查找一次
            cursor = editor.textCursor()
            cursor.movePosition(QTextCursor.Start)
            editor.setTextCursor(cursor)
            if not editor.find(text):
                QMessageBox.information(self, "查找", f"未找到：{text}")

    def caculate_current_row(self):
        """计算当前行的表达式"""
        tab = self.get_current_tab()
        res = tab.evaluate_current_row_expression()
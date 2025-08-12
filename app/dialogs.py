# coding:utf-8
from PySide6.QtWidgets import QDialog, QLineEdit, QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QTextEdit

class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查找")
        self.setFixedWidth(300)
        layout = QHBoxLayout(self)
        self.label = QLabel("查找内容:")
        self.line_edit = QLineEdit()
        self.find_btn = QPushButton("查找下一个")
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.find_btn)
        self.find_btn.clicked.connect(self.accept)

    def get_text(self):
        return self.line_edit.text()

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Markdown 帮助")
        self.setMinimumSize(500, 400)
        layout = QVBoxLayout(self)

        help_text = (
            "# Markdown 基础语法\n"
            "\n"
            "## 标题\n"
            "`# 一级标题`\n"
            "`## 二级标题`\n"
            "`### 三级标题`\n"
            "\n"
            "## 粗体与斜体\n"
            "**粗体**：`**粗体**`\n"
            "*斜体*：`*斜体*`\n"
            "***粗斜体***：`***粗斜体***`\n"
            "\n"
            "## 删除线\n"
            "~~删除线~~：`~~删除线~~`\n"
            "\n"
            "## 列表\n"
            "- 无序列表：`- 项目`\n"
            "1. 有序列表：`1. 项目`\n"
            "\n"
            "## 任务列表\n"
            "- [x] 已完成：`- [x] 已完成`\n"
            "- [ ] 未完成：`- [ ] 未完成`\n"
            "\n"
            "## 引用\n"
            "> 引用内容：`> 引用内容`\n"
            "\n"
            "## 链接与图片\n"
            "[链接文本](https://example.com)：`[链接文本](https://example.com)`\n"
            "![图片alt](url)：`![图片alt](url)`\n"
            "\n"
            "## 代码\n"
            "行内代码：`` `代码` ``\n"
            "代码块：\n"
            "```\n"
            "print('Hello')\n"
            "```\n"
            "\n"
            "## 表格\n"
            "| 表头 | 表头 |\n"
            "| ---- | ---- |\n"
            "| 单元格 | 单元格 |\n"
            "\n"
            "## 分隔线\n"
            "---\n"
        )

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(help_text)  # 只显示纯文本，不渲染
        layout.addWidget(text_edit)

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

class ShortcutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("快捷键一览")
        self.setMinimumSize(400, 350)
        layout = QVBoxLayout(self)

        shortcut_text = (
            "FlashMdPad 常用快捷键：\n"
            "\n"
            "新建标签页：      Ctrl+N\n"
            "打开文件：        Ctrl+O\n"
            "保存：            Ctrl+S\n"
            "另存为：          Ctrl+Shift+S\n"
            "关闭标签页：      Ctrl+W\n"
            "切换标签：        Ctrl+Tab / Ctrl+Shift+Tab\n"
            "查找：            Ctrl+F\n"
            "替换：            Ctrl+H\n"
            "插入当前日期：    Ctrl+D\n"
            "运算表达式：      Ctrl+Enter\n"
            "切换深色模式：    Ctrl+M\n"
            "预览同步滚动：    Ctrl+P\n"
            "Markdown 帮助：   F1\n"
            "快捷键一览：      F2\n"
            "\n"
            ""
        )

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(shortcut_text)
        layout.addWidget(text_edit)

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
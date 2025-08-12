# coding:utf-8

import os
import markdown
from PySide6.QtCore import Qt, QRegularExpression, Signal, QTimer, QUrl
from PySide6.QtGui import (QFont, QTextCharFormat, QColor, QSyntaxHighlighter,QPalette,QKeySequence, QDesktopServices, )
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QSplitter, QPlainTextEdit,
                              QTextBrowser, QFileDialog, QMessageBox)

from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView

from app.constants import LIGHT_THEME_CSS, DARK_THEME_CSS, FONT_FAMILY
from app.editor import CodeEditor
from bleach.sanitizer import Cleaner

class ExternalLinkPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            QDesktopServices.openUrl(url)
            return False  # 阻止 QWebEngineView 自己跳转
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)
    
class MarkdownHighlighter(QSyntaxHighlighter):
    """Markdown语法高亮器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rules = []
        
        # 标题规则
        header_format = QTextCharFormat()
        header_format.setForeground(QColor("#2e7d32"))
        header_format.setFontWeight(QFont.Bold)
        for pattern in [r'^#{1,6}\s+.+$']:
            self._rules.append((QRegularExpression(pattern), header_format))
        
        # 粗体
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        self._rules.append((QRegularExpression(r'\*\*[^\*]+\*\*'), bold_format))
        self._rules.append((QRegularExpression(r'__[^_]+__'), bold_format))
        
        # 斜体
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        self._rules.append((QRegularExpression(r'\*[^\*]+\*'), italic_format))
        self._rules.append((QRegularExpression(r'_[^_]+_'), italic_format))
        
        # 代码块
        code_format = QTextCharFormat()
        code_format.setBackground(QColor("#f5f5f5"))
        code_format.setFontFamily(FONT_FAMILY)
        self._rules.append((QRegularExpression(r'`[^`]+`'), code_format))
        
        # 链接
        link_format = QTextCharFormat()
        link_format.setForeground(QColor("#1565c0"))
        link_format.setFontUnderline(True)
        self._rules.append((QRegularExpression(r'\[[^\]]+\]\([^\)]+\)'), link_format))
        
        # 列表
        list_format = QTextCharFormat()
        list_format.setForeground(QColor("#7b1fa2"))
        for pattern in [r'^[\*\-\+] .+$', r'^\d+\. .+$']:
            self._rules.append((QRegularExpression(pattern), list_format))
    
    def highlightBlock(self, text):
        for pattern, fmt in self._rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class MarkdownTab(QWidget):
    """单个Markdown编辑标签页"""
    modificationChanged = Signal(QWidget)
    def __init__(self, parent=None, file_path=None, dark_mode=False):
        super().__init__(parent)
        self.file_path = file_path
        self.is_modified = False
        self.dark_mode = dark_mode
        self.XSSCleaner = XSSCleaner()
        self.setup_ui()
        
    def setup_ui(self):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 分割器：左侧编辑区，右侧预览区
        splitter = QSplitter(Qt.Horizontal)
        
        # Markdown编辑器
        self.editor = CodeEditor(parent=self,dark_mode=self.dark_mode)
        self.editor.setObjectName("markdownEditor")
        # self.editor.setFont(QFont(FONT_FAMILY, 12))
        self.editor.textChanged.connect(self.update_preview)
        self.editor.textChanged.connect(self.set_modified)
        
        # 语法高亮
        self.highlighter = MarkdownHighlighter(self.editor.document())
        
        # HTML预览
        self.preview = QWebEngineView()
        self.preview.setPage(ExternalLinkPage(self.preview))
        # self.preview.setOpenExternalLinks(True)
        # self.preview.setReadOnly(True)
        # self.preview.document().setDefaultStyleSheet(LIGHT_THEME_CSS)
        
        # 设置预览区域滚动条策略
        # self.preview.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # self.preview.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 添加到分割器
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([600, 400])
        
        layout.addWidget(splitter)
        
        # 如果有文件路径，加载内容
        if self.file_path and os.path.exists(self.file_path):
            self.load_file()
    
    def add_str_to_editor(self, targetstr):
        cursor = self.editor.textCursor()
        cursor.insertText(targetstr)
        self.editor.setTextCursor(cursor)

    def toggle_dark_mode(self, dark_mode):
        """切换深色/浅色模式"""
        self.dark_mode = dark_mode
        self.editor.dark_mode = dark_mode
        self.editor.set_dark_mode(dark_mode)
        if self.dark_mode:
            # self.preview.document().setDefaultStyleSheet(DARK_THEME_CSS)
            # 更新编辑器样式
            palette = self.editor.palette()
            palette.setColor(QPalette.Base, QColor("#2d3748"))
            palette.setColor(QPalette.Text, QColor("#e2e8f0"))
            self.editor.setPalette(palette)
        else:
            # self.preview.document().setDefaultStyleSheet(LIGHT_THEME_CSS)
            # 恢复编辑器样式
            palette = self.editor.palette()
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
            self.editor.setPalette(palette)
        
        # 更新预览
        self.update_preview()

    def load_file(self):
        """从文件加载内容"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.editor.setPlainText(content)
                self.is_modified = False
                self.modificationChanged.emit(self)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法读取文件: {str(e)}")
            return False
    
    def save_file(self):
        """保存文件"""
        if not self.file_path:
            return self.save_as()
            
        try:
            content = self.editor.toPlainText()
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.is_modified = False
            self.modificationChanged.emit(self)
            return True
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")
            return False
    
    def save_as(self):
        """另存为文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存Markdown文件", 
            os.path.expanduser("~"), 
            "Markdown Files (*.md *.markdown);;All Files (*)"
        )
        
        if not file_path:
            return False
        ori_file_path = self.file_path
        self.file_path = file_path #另存为其实为导出功能, 另存为后依旧以保存的文件为主
        self.save_file()
        self.file_path = ori_file_path  # 恢复原文件路径
        return self.save_file()
    
    def evaluate_current_row_expression(self):
        """计算当前行的表达式"""
        self.editor.eval_current_line_and_replace()
        # self.update_preview()
    
    def update_preview(self):
        editor_scrollbar = self.editor.verticalScrollBar()
        if editor_scrollbar.maximum() > 0:
            percent = editor_scrollbar.value() / editor_scrollbar.maximum()
        else:
            percent = 0.0
        percent = min(percent, 1.0)

        markdown_text = self.editor.toPlainText()
        html = markdown.markdown(markdown_text, extensions=['toc','fenced_code', 'tables', 'codehilite', "extra"])
        css = DARK_THEME_CSS if self.dark_mode else LIGHT_THEME_CSS
        html = self.XSSCleaner.safe_markdown(html=html)
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style type="text/css">
        {css}
        </style>
        </head>
        <body>
        <div class="markdown-body">
        {html}
        </div>
        </body>
        </html>
        """

        # 只在内容变化时刷新
        if not hasattr(self, "_last_preview_html") or self._last_preview_html != styled_html:
            self._last_preview_html = styled_html
            self.preview.setHtml(styled_html)

            def scroll_preview():
                if percent >= 0.99:
                    js = """
                    (function() {
                        var h = (document.body ? document.body.scrollHeight : document.documentElement.scrollHeight);
                        window.scrollTo(0, h);
                    })();
                    """
                else:
                    js = f"""
                    (function() {{
                        var body = document.body || document.documentElement;
                        var h = (body ? body.scrollHeight : document.documentElement.scrollHeight) - window.innerHeight;
                        if(h > 0){{
                            window.scrollTo(0, h * {percent});
                        }}
                    }})();
                    """
                self.preview.page().runJavaScript(js)
        try:
            QTimer.singleShot(100, scroll_preview)
        except Exception as e:
            pass  # 可能在某些环境下无法执行JavaScript，忽略错误
    
    def set_modified(self):
        """标记文档已修改"""
        if not self.is_modified:
            self.is_modified = True
            self.modificationChanged.emit(self)


class XSSCleaner(object):
    def __init__(self):
        self.allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol',
            'strong', 'ul', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'br',
            'div', 'span', 'hr', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'del','s'
        ]
        self.allowed_attributes = {
            'a': ['href', 'title'],
            'abbr': ['title'],
            'acronym': ['title'],
            'img': ['src', 'alt', 'title'],
            'table': ['align', 'border'],
            'td': ['align'],
            'th': ['align'],
        }
        self.cleaner = Cleaner(tags=self.allowed_tags,
                        attributes=self.allowed_attributes, 
                        strip=True)
    def safe_markdown(self,html):
        # 清理HTML
        cleaned_html = self.cleaner.clean(html)
        return cleaned_html
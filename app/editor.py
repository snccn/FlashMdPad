# coding:utf-8

from PySide6.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PySide6.QtGui import QFont, QColor,QPainter, QTextFormat
from PySide6.QtCore import Qt, QSize,QRect

class LineNumberArea(QWidget):
    def __init__(self,editor):
        super().__init__(editor)
        self.editor = editor
        self.setFont(QFont("Monospace",10))
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    """带行号功能的代码编辑器"""
    def __init__(self, parent=None, dark_mode=False):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self.setFont(QFont("Monospace", 12))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.dark_mode = dark_mode
        
        # 连接信号
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        # 初始设置
        self.update_line_number_area_width()
        self.highlight_current_line()
    
    def line_number_area_width(self):
        """计算行号区域的宽度"""
        digits = 1
        max_lines = max(1, self.blockCount())
        while max_lines >= 10:
            max_lines /= 10
            digits += 1
        
        # 留出额外空间
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self):
        """更新边距以容纳行号区域"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """更新行号区域"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), 
                                              self.line_number_area_width(), cr.height()))
    
    def line_number_area_paint_event(self, event):
        """绘制行号"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), self.line_number_area.palette().window().color().darker(110))
        
        # 设置字体和颜色
        if self.dark_mode:
            painter.setPen(QColor("#a0aec0"))
        else:
            painter.setPen(QColor("#718096"))
        painter.setFont(self.font())
        
        # 绘制可见行号
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.line_number_area.width() - 5, 
                                self.fontMetrics().height(),
                                Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def highlight_current_line(self):
        """高亮当前行"""
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            if self.dark_mode:
                line_color = QColor("#2d3748").lighter(150)
            else:
                line_color = QColor("#ebf8ff")
            
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)
    
    def set_dark_mode(self, dark_mode):
        """设置深色模式"""
        self.dark_mode = dark_mode
        self.highlight_current_line()
        self.line_number_area.update()

    def get_line_text(self, line_number):
        """获取指定行的文本（行号从0开始计数）"""
        document = self.document()
        
        # 检查行号是否有效
        if line_number < 0 or line_number >= document.blockCount():
            return None
        
        # 获取对应行的文本块
        block = document.findBlockByLineNumber(line_number)
        return block.text()
    
    def replace_line_text(self, line_number, newline):
        return True
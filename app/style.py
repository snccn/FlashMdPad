# coding:utf-8

def apply_global_style(app):
    """应用全局样式表"""
    style = """
    /* 全局样式 */
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 12px;
        background-color: #f5f7fa;
        color: #333;
    }
    
    /* 按钮样式 */
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 500;
        min-width: 80px;
    }
    
    QPushButton:hover {
        background-color: #45a049;
    }
    
    QPushButton:pressed {
        background-color: #3e8e41;
    }
    
    /* 输入框样式 */
    QLineEdit, QTextEdit, QComboBox {
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 6px 10px;
        background-color: white;
    }
    
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #3b82f6;
        outline: none;
    }
    
    /* 标签样式 */
    QLabel {
        color: #374151;
        font-size: 12px;
    }
    
    /* 滚动条样式 */
    QScrollBar:vertical {
        background: #f0f2f5;
        width: 10px;
        margin: 0px 0px 0px 0px;
    }
    
    QScrollBar::handle:vertical {
        background: #cbd5e1;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
    }
    
    /* 选项卡样式 */
    QTabWidget::pane {
        border: 1px solid #d1d5db;
        border-radius: 4px;
        background: white;
    }
    
    QTabBar::tab {
        background: #f1f5f9;
        color: #64748b;
        padding: 8px 16px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        border: 1px solid #d1d5db;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background: white;
        color: #3b82f6;
        border-bottom: 2px solid #3b82f6;
    }
    """
    app.setStyleSheet(style)
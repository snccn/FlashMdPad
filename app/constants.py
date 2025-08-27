# coding:utf-8
import os
import sys

OS_TYPE = sys.platform



if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstaller 临时解压路径
    base_path_execute = os.path.dirname(sys.executable)
else:
    base_path = os.path.realpath(".")
    base_path_execute = base_path

if OS_TYPE == "darwin":
    FONT_FAMILY = "Consolas"
    TOOLBAR_ENABLE = False
    base_path_execute = os.path.expanduser("~/.flashpad/")
    CFG_PATH = os.path.join(base_path_execute,'config.ini')
elif OS_TYPE == "win32":
    FONT_FAMILY = "Microsoft YaHei"
    TOOLBAR_ENABLE = True
    os.path.realpath(base_path_execute)
    CFG_PATH = os.path.join(base_path_execute,'config.ini')
else:
    base_path_execute = os.path.expanduser("~/.flashpad/")
    CFG_PATH = os.path.join(base_path_execute,'config.ini')
    FONT_FAMILY = "Arial"

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

CFG_GENERAL_SECTION = "app"
FONT_SIZE = 12

KEY_FONT_FAMILY = "font_family"
KEY_FONT_SIZE = "font_size"
KEY_TOOLBAR_ENABLE = "toolbar"
KEY_APPSTYLE = "app_style"
KEY_WORKSPACE = "work_path"
KEY_LIGHT_THEME_CSS = "theme_css"
KEY_DARK_THEME_CSS = "theme_dark_css"
KEY_DARK_MODE = "darkmode"

LIGHT_THEME_CSS = """
/* 全局基础样式 - 极简核心 */
body {
    margin: 0;
    padding: 0;
    background-color: #ffffff;
    color: #24292e;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.5; /* 保证阅读流畅性的核心行高 */
}

/* 内容容器 - 聚焦阅读区域 */
.markdown-body {
    max-width: 880px; /* 适度收窄宽度，减少视线跨度 */
    margin: 0 auto;
    padding: 32px 24px; /* 上下留足呼吸感，左右适配窄屏 */
    background: #ffffff;
}

/* 标题样式 - 层级清晰无冗余 */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    margin-top: 28px;
    margin-bottom: 12px;
    line-height: 1.2; /* 标题更紧凑 */
    color: #24292e;
}

/* 仅h1/h2保留下划线，区分核心层级 */
h1 {
    font-size: 2em;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.2em;
}

h2 {
    font-size: 1.5em;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.2em;
}

/* 次级标题简化，无下划线 */
h3 { font-size: 1.25em; }
h4 { font-size: 1em; }
h5 { font-size: 0.875em; }
h6 { font-size: 0.85em; color: #6a737d; } /* 仅h6降色，突出层级 */

/* 文本元素 - 去装饰，重内容 */
p {
    margin: 0 0 14px 0; /* 统一段落间距，避免拥挤 */
}

strong { color: #24292e; } /* 保持强调色与正文一致，仅靠字重突出 */
em { color: #24292e; font-style: italic; } /* 仅保留斜体，无额外色值 */
del, s { color: #6a737d; text-decoration: line-through; } /* 简化删除线样式 */

/* 代码块 - 轻量突出，不抢视线 */
pre, code {
    font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 14px;
}

pre {
    background: #f6f8fa;
    border-radius: 3px; /* 极小圆角，弱化边框感 */
    padding: 14px;
    overflow: auto;
    margin: 0 0 14px 0;
}

code {
    background: rgba(27, 31, 35, 0.05);
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 85%; /* 相对父元素微调，保持协调 */
}

/* 引用 - 极简边框，无多余背景 */
blockquote {
    border-left: 3px solid #eaecef; /* 减窄边框，更内敛 */
    color: #6a737d;
    padding: 0 1em;
    margin: 0 0 14px 0;
}

/* 列表 - 精简间距，提升可读性 */
ul, ol {
    margin: 0 0 14px 0;
    padding-left: 1.8em; /* 适度缩进，避免过宽 */
}

ul li, ol li {
    margin-bottom: 0.2em; /* 减少列表项间距，更紧凑 */
}

/* 嵌套列表无额外间距，保持层级干净 */
ul ul, ol ul, ul ol, ol ol {
    margin: 0;
    padding-left: 1.2em;
}

/* 任务列表 - 简化样式，聚焦勾选状态 */
.markdown-body input[type="checkbox"] {
    width: 1em;
    height: 1em;
    margin-right: 6px;
    vertical-align: middle;
    accent-color: #2eaadc;
    pointer-events: none;
}

/* 表格 - 去阴影，轻边框 */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 0 0 14px 0;
}

th, td {
    border: 1px solid #eaecef; /* 细边框，减少厚重感 */
    padding: 6px 12px; /* 精简内边距，避免表格过宽 */
    text-align: left;
}

th {
    background: #f6f8fa;
    font-weight: 600;
}

/* 偶数行背景简化，仅轻微区分 */
tr:nth-child(even) {
    background: #f6f8fa;
}

/* 链接 - 弱化 hover 变化，保持稳定感 */
a {
    color: #0366d6;
    text-decoration: none;
}

a:hover {
    text-decoration: underline; /* 仅添加下划线，无额外色变 */
}

/* 水平线 - 极简线条 */
hr {
    border: 0;
    height: 1px;
    background: #eaecef;
    margin: 24px 0;
}

/* 脚注 - 简化样式，与链接统一 */
sup {
    font-size: 0.85em;
    color: #0366d6;
    vertical-align: super;
}

/* 图片 - 纯净展示，无多余装饰 */
img {
    max-width: 100%;
    box-sizing: border-box;
    background-color: #ffffff;
    margin: 0 0 14px 0; /* 统一图片间距 */
}

/* 暗色模式 - 同步简约风格，仅调整核心色值 */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #0d1117;
        color: #c9d1d9;
    }

    .markdown-body {
        background: #0d1117;
    }

    h1, h2, h3, h4, h5 {
        color: #c9d1d9;
        border-bottom-color: #21262d;
    }

    h6 {
        color: #8b949e;
    }

    pre {
        background: #161b22;
    }

    code {
        background: rgba(110, 118, 129, 0.4);
        color: #c9d1d9;
    }

    blockquote {
        border-left-color: #30363d;
        color: #8b949e;
    }

    table {
        border-color: #30363d;
    }

    th, td {
        border-color: #30363d;
    }

    th, tr:nth-child(even) {
        background: #161b22;
    }

    a {
        color: #58a6ff;
    }

    hr {
        background: #30363d;
    }

    img {
        background-color: #0d1117;
    }
}

"""

DARK_THEME_CSS = """
/* 全局基础样式 - 极简核心（浅色模式保留原逻辑，此处仅展示深色模式优化） */
/* 内容容器 - 聚焦阅读区域 */
.markdown-body {
    max-width: 880px; /* 适度收窄宽度，减少视线跨度 */
    margin: 0 auto;
    padding: 32px 24px; /* 上下留足呼吸感，左右适配窄屏 */
    background: #121212;
}

body {
    background-color: #121212; /* 比GitHub默认#0d1117稍浅，更柔和 */
    color: #e0e0e0; /* 正文色：浅灰而非纯白，降低强光刺激 */
}


/* 2. 标题层级：通过微妙色阶区分，避免同色单调 */
h1, h2, h3, h4, h5 {
    color: #f5f5f5; /* 主标题稍亮，提升辨识度 */
    border-bottom-color: #2d2d2d; /* 下划线：深灰而非黑，弱化分割感 */
}

h6 {
    color: #a0a0a0; /* 次级标题降色，明确层级 */
}

/* 3. 代码块：暗部细节优化，避免模糊 */
pre {
    background: #1e1e1e; /* 代码块底色：比页面深一级，形成轻微层次 */
    border: 1px solid #2d2d2d; /* 细边框：区分代码块与正文，不突兀 */
}

code {
    background: rgba(70, 70, 70, 0.3); /* 行内代码背景：半透明，不抢视线 */
    color: #d4d4d4; /* 代码色：比正文稍浅，保持可读性 */
}

/* 4. 引用：弱化边框，统一色调 */
blockquote {
    border-left-color: #3d3d3d; /* 引用边框：浅灰，避免深色中过扎眼 */
    color: #b0b0b0; /* 引用文本：比正文暗一级，明确区分引用属性 */
}

/* 5. 表格：柔和对比，避免刺眼 */
table {
    border-color: #2d2d2d; /* 表格边框：与标题下划线同色，统一风格 */
}

th, td {
    border-color: #2d2d2d;
}

th {
    background: #1e1e1e; /* 表头底色：与代码块一致，视觉统一 */
    color: #f0f0f0; /* 表头文字稍亮，突出表头功能 */
}

tr:nth-child(even) {
    background: #181818; /* 偶数行底色：比页面深一点，区分行但不割裂 */
}

/* 6. 链接：低饱和蓝，避免高饱和色刺眼 */
a {
    color: #8ab4f8; /* 比GitHub默认#58a6ff稍暗，更柔和 */
}

a:hover {
    color: #a8c7ff; /* hover时轻微提亮，反馈清晰但不突兀 */
    text-decoration: underline;
}

/* 7. 水平线：弱化分割，保持协调 */
hr {
    background: #2d2d2d; /* 与标题下划线同色，统一视觉语言 */
}

/* 8. 图片：适配暗背景，避免白边突兀 */
img {
    background-color: #121212; /* 与页面底色一致，避免图片透明时露白 */
    /* 可选：为图片添加细边框，暗背景下更清晰 */
    border: 1px solid rgba(70, 70, 70, 0.2);
}

/* 9. 任务列表：勾选框优化，暗部更清晰 */
.markdown-body input[type="checkbox"] {
    accent-color: #8ab4f8; /* 勾选色与链接色统一，风格一致 */
    background-color: #1e1e1e; /* 未勾选框底色：与代码块一致 */
    border: 1px solid #3d3d3d; /* 边框：区分勾选框与背景 */
}

"""
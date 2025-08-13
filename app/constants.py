# coding:utf-8
import os
import sys

OS_TYPE = sys.platform

if OS_TYPE == "darwin":
    FONT_FAMILY = "PingFang SC"
elif OS_TYPE == "win32":
    FONT_FAMILY = "Microsoft YaHei"
else:
    FONT_FAMILY = "Arial"

LIGHT_THEME_CSS = """
/* 基础样式调整 - 更贴近GitHub风格 */
body {
    background-color: #ffffff; /* GitHub 浅色模式背景 */
    color: #24292e; /* GitHub 主要文本色 */
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    line-height: 1.5; /* GitHub 行高 */
    font-size: 16px;
    margin: 0;
    padding: 0;
}

.markdown-body {
    max-width: 980px; /* GitHub 内容最大宽度 */
    margin: 0 auto;
    padding: 45px; /* GitHub 内边距 */
    background: #ffffff;
    border-radius: 0; /* 移除圆角，GitHub 无圆角 */
    box-shadow: none; /* 移除阴影 */
}

/* 标题样式 - 调整颜色和间距 */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600; /* GitHub 标题字重 */
    #margin-top: 24px;
    margin-bottom: 16px;
    line-height: 1.25;
}

h1 { 
    font-size: 2em; 
    color: #24292e; 
    border-bottom: 1px solid #eaecef; /* 标题下划线 */
    padding-bottom: 0.3em;
}
h2 { 
    font-size: 1.5em; 
    color: #24292e; 
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
}
h3 { font-size: 1.25em; color: #24292e; }
h4 { font-size: 1em; color: #24292e; }
h5 { font-size: 0.875em; color: #24292e; }
h6 { font-size: 0.85em; color: #6a737d; }

/* 段落和文本 */
p { 
    margin-top: 0;
    margin-bottom: 16px; /* GitHub 段落间距 */
}
strong { color: #24292e; }
em { color: #24292e; }
del, s { color: #6a737d; text-decoration: line-through; }

/* 代码块和行内代码 - 关键调整 */
pre, code {
    font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 12px; /* GitHub 代码字体大小 */
}
pre {
    background: #f6f8fa;
    border-radius: 3px; /* 更小圆角 */
    padding: 16px;
    overflow: auto;
    margin-bottom: 16px;
    border-left: none; /* 移除左侧边框 */
    word-wrap: normal;
}
code {
    background: rgba(27, 31, 35, 0.05);
    color: #24292e;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 85%; /* 相对父元素的85% */
}

/* 引用 */
blockquote {
    border-left: 4px solid #eaecef; /* GitHub 引用边框色 */
    background: transparent; /* 移除背景色 */
    color: #6a737d;
    padding: 0 1em;
    margin: 0 0 16px 0;
    border-radius: 0;
    font-style: normal; /* 移除斜体 */
}

/* 列表 */
ul, ol {
    margin-bottom: 16px;
    padding-left: 2em;
    margin-top: 0;
}
ul li, ol li {
    margin-bottom: 0.25em;
}
ul ul, ol ul, ul ol, ol ol {
    margin-bottom: 0;
    margin-top: 0;
}

/* 任务列表 */
.markdown-body input[type="checkbox"] {
    width: 1em;
    height: 1em;
    margin-right: 6px;
    vertical-align: middle;
    accent-color: #2eaadc;
    pointer-events: none;
}

/* 表格 */
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 16px;
    background: transparent;
    border-radius: 0;
    overflow: visible;
    box-shadow: none;
}
th, td {
    border: 1px solid #eaecef;
    padding: 6px 13px;
    text-align: left;
}
th {
    background: #f6f8fa;
    font-weight: 600;
    color: #24292e;
}
tr:nth-child(even) {
    background: #f6f8fa;
}

/* 链接 */
a {
    color: #0366d6; /* GitHub 链接色 */
    text-decoration: none;
}
a:hover {
    color: #0366d6;
    text-decoration: underline;
}

/* 水平线 */
hr {
    border: 0;
    height: 1px;
    background: #eaecef;
    margin: 24px 0;
}

/* 脚注 */
sup {
    font-size: 0.85em;
    color: #0366d6;
}

/* 图片样式 */
img {
    max-width: 100%;
    box-sizing: content-box;
    background-color: #ffffff;
}

/* 暗色模式调整 - 贴近GitHub Dark */
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
    th {
        background: #161b22;
        color: #c9d1d9;
    }
    tr:nth-child(even) {
        background: #161b22;
    }
    a {
        color: #58a6ff;
    }
    a:hover {
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
/* 深色模式样式表 - 高对比度版本 */
body {
    background-color: #121212;
    color: #e0e0e0;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    font-size: 16px;
    margin: 0;
    padding: 0;
}

.markdown-body {
    max-width: 900px;
    margin: 0 auto;
    padding: 30px;
    background-color: #1e1e1e;
    border-radius: 4px;
}

/* 标题样式 */
h1, h2, h3, h4, h5, h6 {
    color: #bb86fc;
    margin-top: 1.8em;
    margin-bottom: 0.8em;
    font-weight: 600;
}

h1 {
    font-size: 2em;
    border-bottom: 1px solid #333;
    padding-bottom: 0.3em;
}

h2 {
    font-size: 1.6em;
    border-bottom: 1px solid #333;
    padding-bottom: 0.2em;
}

h3 { font-size: 1.3em; color: #9d4edd; }
h4 { font-size: 1.1em; color: #9d4edd; }
h5 { font-size: 1em; color: #7b2cbf; }
h6 { font-size: 0.9em; color: #7b2cbf; }

/* 文本样式 */
p {
    margin-bottom: 1em;
}

strong {
    color: #f5f5f5;
    font-weight: 600;
}

em {
    color: #f0a988;
    font-style: italic;
}

del {
    color: #6c757d;
    text-decoration: line-through;
}

/* 代码样式 */
pre, code {
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-size: 14px;
}

pre {
    background-color: #121212;
    border-radius: 4px;
    padding: 16px;
    overflow-x: auto;
    margin: 1.5em 0;
    border: 1px solid #333;
}

code {
    background-color: #2d2d2d;
    color: #dcdcaa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

/* 引用样式 */
blockquote {
    border-left: 3px solid #bb86fc;
    padding: 0.5em 1em;
    margin: 1em 0;
    background-color: #2d2d2d;
    color: #d0d0d0;
    border-radius: 0 4px 4px 0;
}

/* 列表样式 */
ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin-bottom: 0.5em;
}

li::marker {
    color: #bb86fc;
}

/* 任务列表 */
input[type="checkbox"] {
    accent-color: #03dac6;
    margin-right: 0.5em;
}

/* 表格样式 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
}

th, td {
    border: 1px solid #333;
    padding: 0.8em 1em;
    text-align: left;
}

th {
    background-color: #2d2d2d;
    color: #03dac6;
    font-weight: 600;
}

tr:nth-child(even) {
    background-color: #252525;
}

/* 链接样式 */
a {
    color: #03a9f4;
    text-decoration: none;
}

a:hover {
    color: #2196f3;
    text-decoration: underline;
}

/* 水平线 */
hr {
    border: none;
    border-top: 1px solid #333;
    margin: 2em 0;
}

/* 图片样式 */
img {
    max-width: 100%;
    border-radius: 4px;
    background-color: #2d2d2d;
    padding: 4px;
    border: 1px solid #333;
}
"""
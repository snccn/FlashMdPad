# coding:utf-8
import os
import sys

OS_TYPE = sys.platform

if OS_TYPE == "darwin":
    FONT_FAMILY = "PingFang SC"
elif OS_TYPE == "Windows":
    FONT_FAMILY = "Microsoft YaHei"
else:
    FONT_FAMILY = "Arial"

LIGHT_THEME_CSS = """
body {
    background-color: #f8f9fa;
    color: #212529;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.7;
    font-size: 16px;
    margin: 0;
}
.markdown-body {
    padding: 24px 16px;
    min-height: 100vh;
    max-width: 900px;
    margin: auto;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* 标题 */
h1, h2, h3, h4, h5, h6 {
    font-weight: bold;
    margin-top: 2em;
    margin-bottom: 1em;
    line-height: 1.25;
}
h1 { font-size: 2.2em; color: #1a365d; border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }
h2 { font-size: 1.7em; color: #2c5282; border-bottom: 1px solid #eaeaea; padding-bottom: 8px; }
h3 { font-size: 1.3em; color: #2b6cb0; }
h4 { font-size: 1.1em; color: #3182ce; }
h5 { font-size: 1em; color: #4299e1; }
h6 { font-size: 0.95em; color: #63b3ed; }

/* 段落和文本 */
p { margin-bottom: 1em; }
strong { color: #2d3748; }
em { color: #4a5568; }
del, s { color: #a0aec0; text-decoration: line-through; }

/* 代码块和行内代码 */
pre, code {
    font-family: 'Fira Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}
pre {
    background: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow: auto;
    margin-bottom: 1.5em;
    font-size: 0.97em;
    border-left: 4px solid #4299e1;
}
code {
    background: #f1f3f5;
    color: #d6336c;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.97em;
}

/* 引用 */
blockquote {
    border-left: 4px solid #4299e1;
    background: #f1f5f9;
    color: #4a5568;
    padding: 12px 18px;
    margin: 1.5em 0;
    border-radius: 4px;
    font-style: italic;
}

/* 列表 */
ul, ol {
    margin-bottom: 1em;
    padding-left: 2em;
}
ul li, ol li {
    margin-bottom: 0.4em;
}
ul ul, ol ul, ul ol, ol ol {
    margin-bottom: 0;
}

/* 任务列表 */
.markdown-body input[type="checkbox"] {
    width: 1.1em;
    height: 1.1em;
    margin-right: 8px;
    vertical-align: middle;
    accent-color: #4299e1;
    pointer-events: none;
}

/* 表格 */
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 1.5em;
    background: #fff;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
th, td {
    border: 1px solid #e2e8f0;
    padding: 10px 14px;
    text-align: left;
}
th {
    background: #f1f5f9;
    font-weight: bold;
    color: #2c5282;
}
tr:nth-child(even) {
    background: #f7fafc;
}

/* 链接 */
a {
    color: #3182ce;
    text-decoration: none;
    transition: color 0.2s;
}
a:hover {
    color: #63b3ed;
    text-decoration: underline;
}

/* 水平线 */
hr {
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 2em 0;
}

/* 脚注 */
sup {
    font-size: 0.8em;
    color: #4299e1;
}
"""

DARK_THEME_CSS = """
body {
    background-color: #23272e;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.7;
    font-size: 16px;
    margin: 0;
}
.markdown-body {
    padding: 24px 16px;
    max-width: 900px;
    margin: auto;
    background: #2d3748;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.10);
}

/* 标题 */
h1, h2, h3, h4, h5, h6 {
    font-weight: bold;
    margin-top: 2em;
    margin-bottom: 1em;
    line-height: 1.25;
}
h1 { font-size: 2.2em; color: #81e6d9; border-bottom: 2px solid #4a5568; padding-bottom: 10px; }
h2 { font-size: 1.7em; color: #4fd1c5; border-bottom: 1px solid #4a5568; padding-bottom: 8px; }
h3 { font-size: 1.3em; color: #38b2ac; }
h4 { font-size: 1.1em; color: #319795; }
h5 { font-size: 1em; color: #2c7a7b; }
h6 { font-size: 0.95em; color: #285e61; }

/* 段落和文本 */
p { margin-bottom: 1em; }
strong { color: #faf089; }
em { color: #fbd38d; }
del, s { color: #718096; text-decoration: line-through; }

/* 代码块和行内代码 */
pre, code {
    font-family: 'Fira Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}
pre {
    background: #23272e;
    border-radius: 6px;
    padding: 16px;
    overflow: auto;
    margin-bottom: 1.5em;
    font-size: 0.97em;
    border-left: 4px solid #63b3ed;
}
code {
    background: #2d3748;
    color: #fbd38d;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.97em;
}

/* 引用 */
blockquote {
    border-left: 4px solid #4fd1c5;
    background: #23272e;
    color: #cbd5e0;
    padding: 12px 18px;
    margin: 1.5em 0;
    border-radius: 4px;
    font-style: italic;
}

/* 列表 */
ul, ol {
    margin-bottom: 1em;
    padding-left: 2em;
}
ul li, ol li {
    margin-bottom: 0.4em;
}
ul ul, ol ul, ul ol, ol ol {
    margin-bottom: 0;
}

/* 任务列表 */
.markdown-body input[type="checkbox"] {
    width: 1.1em;
    height: 1.1em;
    margin-right: 8px;
    vertical-align: middle;
    accent-color: #63b3ed;
    pointer-events: none;
}

/* 表格 */
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 1.5em;
    background: #2d3748;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
}
th, td {
    border: 1px solid #4a5568;
    padding: 10px 14px;
    text-align: left;
}
th {
    background: #23272e;
    font-weight: bold;
    color: #81e6d9;
}
tr:nth-child(even) {
    background: #23272e;
}

/* 链接 */
a {
    color: #63b3ed;
    text-decoration: none;
    transition: color 0.2s;
}
a:hover {
    color: #90cdf4;
    text-decoration: underline;
}

/* 水平线 */
hr {
    border: 0;
    height: 1px;
    background: #4a5568;
    margin: 2em 0;
}

/* 脚注 */
sup {
    font-size: 0.8em;
    color: #4fd1c5;
}
"""
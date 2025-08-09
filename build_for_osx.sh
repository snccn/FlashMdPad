#!/bin/bash

# # 1. 创建虚拟环境
# python3 -m venv build_env
# source build_env/bin/activate

# # 2. 安装依赖
# pip install -r requirements.txt
# pip install --upgrade pyinstaller

# # 3. 获取Python路径
# PYTHON_PATH=$(dirname $(which python3))/../Frameworks/Python.framework/Versions/Current/Python

# 4. 打包应用
pyinstaller FlashMdPad.spec

# # 5. 手动修复
# cp $PYTHON_PATH dist/FlashMdPad.app/Contents/MacOS/
# install_name_tool -change \
#   $PYTHON_PATH \
#   @executable_path/Python \
#   dist/FlashMdPad.app/Contents/MacOS/MyApp

# 6. 代码签名
codesign --force --deep --sign - \
  --entitlements ./resources/entitlements.plist \
  dist/FlashMdPad.app

# 7. 验证
open dist/FlashMdPad.app
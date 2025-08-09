# -*- mode: python ; coding: utf-8 -*-

resources = [
    ('resources/icons/icon.png', 'resources/icons'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=resources,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FlashMdPad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FlashMdPad',
)
app = BUNDLE(
    coll,
    name='FlashMdPad.app',
    icon="resources/icons/icon.icns",
    bundle_identifier="top.yamisn.flashmdpad",
    info_plist={
        'LSUIElement': '1',
    }
)

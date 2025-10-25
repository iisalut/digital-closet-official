# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['closet_app.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/tulasii/PyCharmMiscProject/.venv/lib/python3.13/site-packages/rfc3987_syntax/syntax_rfc3987.lark', 'rfc3987_syntax')],
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
    a.binaries,
    a.datas,
    [],
    name='closet_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='closet_app.app',
    icon=None,
    bundle_identifier=None,
)

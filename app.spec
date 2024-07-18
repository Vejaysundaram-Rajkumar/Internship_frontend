# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\projects\\Internship_frontend\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\projects\\Internship_frontend\\Templates', 'Templates/'), ('D:\\projects\\Internship_frontend\\uploads', 'uploads/'), ('D:\\projects\\Internship_frontend\\main.py', '.'), ('D:\\projects\\Internship_frontend\\transcription', 'transcription/'), ('D:\\projects\\Internship_frontend\\static', 'static/'), ('D:\\projects\\Internship_frontend\\translation_nllb', 'translation_nllb/')],
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
    name='app',
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
    icon=['D:\\College\\Kavuery Hospital Internship\\logo.ico'],
)

# uvv_toolkit.spec

from PyInstaller.utils.hooks import collect_submodules
import pathlib

project_dir = str(pathlib.Path.cwd())
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[project_dir],
    binaries=[],
    datas=[('require-style.css', '.')],
    hiddenimports=collect_submodules('menu'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='UVV_Toolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None
)

from pathlib import Path
import shutil
import sys
import os
import platform
import re
import subprocess

# Detect platform
current_platform = platform.system()

# Read VERSION from main.py
with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()
    match = re.search(r'VERSION\s*=\s*["\']v?(\d+\.\d+\.\d+)["\']', content)
    if not match:
        print("❌ Não foi possível extrair a versão do main.py")
        sys.exit(1)
    version = match.group(1)

output_dir = Path("dist")
output_dir.mkdir(exist_ok=True)

# Choose PyInstaller command
pyinstaller_cmd = [
    "pyinstaller",
    "uvv_toolkit.spec",
    "--clean"
]

print(f"📦 Compilando versão v{version} para {current_platform}...")

# Run PyInstaller
subprocess.run(pyinstaller_cmd, check=True)

# Define expected output name
if current_platform == "Windows":
    built_file = output_dir / "UVV_Toolkit.exe"
    target_file = output_dir / f"UVV_Toolkit-v{version}.exe"
elif current_platform == "Darwin":
    built_file = output_dir / "UVV_Toolkit"
    target_file = output_dir / f"UVV_Toolkit-v{version}.app"
else:
    built_file = output_dir / "UVV_Toolkit"
    target_file = output_dir / f"UVV_Toolkit-v{version}.elf"

# Rename output binary
if built_file.exists():
    if target_file.exists():
        target_file.unlink()
    shutil.move(str(built_file), str(target_file))
    print(f"✅ Binário final: {target_file}")
else:
    print(f"❌ Arquivo de saída não encontrado: {built_file}")
    sys.exit(1)

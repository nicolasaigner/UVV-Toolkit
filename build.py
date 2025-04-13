import os
import sys
import shutil
import platform
import subprocess
import re
from pathlib import Path

def get_version_from_main():
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
        match = re.search(r'VERSION\s*=\s*[\'"]([^\'"]+)[\'"]', content)
        if match:
            return match.group(1)
        raise RuntimeError("Versão não encontrada em main.py")

def get_platform_tag():
    system = platform.system().lower()
    arch = platform.machine().lower()

    if system == "windows":
        return "win_x86_64"
    elif system == "linux":
        return "linux_x86_64"
    elif system == "darwin":
        return "universal_apple_darwin"
    else:
        raise RuntimeError(f"Sistema operacional '{system}' não suportado")

def get_output_filename(version):
    platform_tag = get_platform_tag()

    if "windows" in platform_tag:
        ext = ".exe"
    elif "darwin" in platform_tag:
        ext = ".app"
    else:
        ext = ""  # Linux geralmente é binário sem extensão

    return f"UVV_Toolkit_{platform_tag}-{version}{ext}"

def build():
    version = get_version_from_main()
    print(f"[INFO] Versão detectada: {version}")

    # Remove build antigos
    for pasta in ["build", "dist"]:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
            print(f"[INFO] Diretório removido: {pasta}")

    # Executa o PyInstaller
    print("[INFO] Iniciando build com PyInstaller...")
    subprocess.run(["pyinstaller", "uvv_toolkit.spec"], check=True)

    # Renomeia o executável final
    output_name = get_output_filename(version)
    dist_path = Path("dist") / "UVV_Toolkit"

    if platform.system().lower() == "windows":
        src = dist_path / "UVV_Toolkit.exe"
    elif platform.system().lower() == "darwin":
        src = dist_path / "UVV_Toolkit.app"
    else:
        src = dist_path / "UVV_Toolkit"

    dest = Path("dist") / output_name

    if not src.exists():
        raise FileNotFoundError(f"Arquivo de saída esperado não encontrado: {src}")

    shutil.move(str(src), str(dest))
    print(f"[✔] Build finalizado: {dest}")

if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"[ERRO] {e}")
        sys.exit(1)

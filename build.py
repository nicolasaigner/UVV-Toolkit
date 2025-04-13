import sys
import shutil
import subprocess
import platform
import re
from pathlib import Path

def obter_versao_do_main():
    main_path = Path("main.py")
    conteudo = main_path.read_text(encoding="utf-8")
    match = re.search(r'VERSION\s*=\s*"([^"]+)"', conteudo)
    if not match:
        raise ValueError("Não foi possível encontrar a versão em main.py")
    return match.group(1)

def nome_final(sistema, versao):
    base = "UVV_Toolkit"
    if sistema == "Windows":
        return f"{base}_win_x86_64-{versao}.exe"
    elif sistema == "Linux":
        return f"{base}_linux_x86_64-{versao}"
    elif sistema == "Darwin":
        return f"{base}_universal_apple_darwin-{versao}.app"
    else:
        raise RuntimeError(f"Sistema operacional não suportado: {sistema}")

def main():
    versao = obter_versao_do_main()
    print(f"[INFO] Versão detectada: {versao}")

    build_dir = Path("build")
    dist_dir = Path("dist")

    for pasta in [build_dir, dist_dir]:
        if pasta.exists():
            shutil.rmtree(pasta)
            print(f"[INFO] Diretório removido: {pasta}")

    print("[INFO] Iniciando build com PyInstaller...")
    subprocess.run(["pyinstaller", "uvv_toolkit.spec"], check=True)

    sistema = platform.system()
    print(f"[INFO] Sistema detectado: {sistema}")

    if sistema == "Windows":
        original = dist_dir / "UVV_Toolkit.exe"
    else:
        original = dist_dir / "UVV_Toolkit"

    if not original.exists():
        raise FileNotFoundError(f"[ERRO] Arquivo de saída esperado não encontrado: {original}")

    novo_nome = dist_dir / nome_final(sistema, versao)
    original.rename(novo_nome)

    print(f"[OK] Build concluído com sucesso: {novo_nome}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FALHA] {e}")
        sys.exit(1)

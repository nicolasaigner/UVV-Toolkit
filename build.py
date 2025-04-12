import os
import subprocess
import time

EXE_NAME = "UVV_Toolkit.exe"
DIST_PATH = os.path.join("dist", EXE_NAME)
SPEC_FILE = "uvv_toolkit.spec"

def kill_if_running():
    print("[*] Verificando se o executável está em uso...")
    try:
        subprocess.run(["taskkill", "/f", "/im", EXE_NAME], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[✔] Processo encerrado.")
    except subprocess.CalledProcessError:
        print("[•] Nenhum processo em execução.")

def delete_old_exe():
    if os.path.exists(DIST_PATH):
        try:
            os.remove(DIST_PATH)
            print(f"[✔] EXE antigo removido: {DIST_PATH}")
        except Exception as e:
            print(f"[✘] Não foi possível remover {DIST_PATH}: {e}")
            print("Tentando encerrar processo e tentar novamente...")
            kill_if_running()
            time.sleep(1)
            os.remove(DIST_PATH)
            print(f"[✔] Removido após matar processo.")

def build_exe():
    print("[*] Iniciando build com PyInstaller...")
    result = subprocess.call(f"pyinstaller {SPEC_FILE} --clean", shell=True)
    if result == 0:
        print("[✔] Build finalizado com sucesso.")
    else:
        print("[✘] Build falhou. Veja as mensagens acima.")

if __name__ == "__main__":
    print("🔧 UVV Toolkit - Build Script\n")
    delete_old_exe()
    build_exe()

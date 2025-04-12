import subprocess
import sys

from dotenv import load_dotenv

import menu

# Carrega variáveis de ambiente do .env
load_dotenv()

# ========== APRESENTAÇÃO ==========
SOFTWARE_NAME = "UVV CLI Toolkit"
VERSION = "v1.0.0"

HEADER = f"""
{'=' * 50}
  {SOFTWARE_NAME} - {VERSION}
  Utilitário CLI para tarefas automatizadas do Portal UVV
{'=' * 50}
"""

# Define as opções do menu com seus respectivos scripts
menu_options = [
    ("Buscar Provas Corrigidas", "busca_provas_corrigidas.py"),
    ("Transformar provas em PDF", None),
    # ("Buscar AOPs", None),

    # ("Gerar um Flip Card para estudar", None),
    ("Sair", "exit")
]


def executar_opcao(label, script):
    if script == "exit":
        print("Saindo...")
        sys.exit(0)
    elif script:
        subprocess.run([sys.executable, script])
        input("\nPressione Enter para voltar ao menu...")
    else:
        input(f"\n[!] '{label}' ainda não implementado. Pressione Enter para voltar...")


def main():
    while True:
        # Define as opções de menu
        opcoes_menu = [label for label, _ in menu_options]

        # Cria o menu com pretext como cabeçalho
        menu_cli = menu.Menu(opcoes_menu, color=menu.Colors.CYAN, style=menu.Styles.SELECTED, pretext=HEADER, ).launch(
            response="Index")
        # escolha_index = menu_cli.launch(response="Index")

        # Recupera e executa a opção escolhida
        label, script = menu_options[menu_cli]
        executar_opcao(label, script)


if __name__ == "__main__":
    main()

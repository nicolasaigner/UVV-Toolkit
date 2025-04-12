import sys
import json
import menu
import busca_provas_corrigidas

SOFTWARE_NAME = "UVV CLI Toolkit"
VERSION = "v1.0.0"

HEADER = f"""
{'=' * 50}
  {SOFTWARE_NAME} - {VERSION}
  Utilitário CLI para tarefas automatizadas do Portal UVV
{'=' * 50}
"""

CONFIG_FILE = "config.json"

menu_options = [
    ("Buscar Provas Corrigidas", "busca_provas"),
    # ("Transformar provas em PDF", None),
    ("Configurações do Usuário", "config"),
    ("Sair", "exit")
]

def configurar_usuario():
    print("\n[🛠] Configurações do Usuário\n")
    matricula = input("Digite sua matrícula: ").strip()
    senha = input("Digite sua senha: ").strip()

    config_data = {
        "matricula": matricula,
        "senha": senha,
        "reset": False,
        "debug": False
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

    print("\n[✔] Configuração salva com sucesso!")
    input("Pressione Enter para voltar ao menu...")

def executar_opcao(label, chave):
    if chave == "exit":
        print("Saindo...")
        sys.exit(0)
    elif chave == "config":
        configurar_usuario()
    elif chave == "busca_provas":
        busca_provas_corrigidas.run()
        input("\nPressione Enter para voltar ao menu...")
    else:
        input(f"\n[!] '{label}' ainda não implementado. Pressione Enter para voltar...")

def main():
    while True:
        opcoes_menu = [label for label, _ in menu_options]
        escolha_index = menu.Menu(opcoes_menu, color=menu.Colors.CYAN, style=menu.Styles.SELECTED, pretext=HEADER).launch(response="Index")
        label, chave = menu_options[escolha_index]
        executar_opcao(label, chave)

if __name__ == "__main__":
    main()

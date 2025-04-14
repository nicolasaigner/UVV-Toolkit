# UVV CLI Toolkit

![GitHub Release](https://img.shields.io/github/v/release/nicolasaigner/UVV-Toolkit?label=Vers%C3%A3o%20Est%C3%A1vel)
![Custom Badge](https://img.shields.io/badge/Plataforma_suportada-Windows_(.exe)-blue)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/nicolasaigner/UVV-Toolkit/latest/total?label=Downloads&color=25c2a0)
![GitHub Release Date](https://img.shields.io/github/release-date/nicolasaigner/UVV-Toolkit?label=Data%20do%20lan%C3%A7amento)
![GitHub top language](https://img.shields.io/github/languages/top/nicolasaigner/UVV-Toolkit)
[![Build and Release UVV CLI Toolkit](https://github.com/nicolasaigner/UVV-Toolkit/actions/workflows/build-release.yml/badge.svg?branch=main)](https://github.com/nicolasaigner/UVV-Toolkit/actions/workflows/build-release.yml)



## 📘 Descrição

O **UVV CLI Toolkit** é um utilitário de linha de comando desenvolvido para automatizar tarefas comuns do portal de aluno da [Universidade Vila Velha (UVV)](https://aluno.uvv.br/). A principal funcionalidade atual é o **download automatizado de provas corrigidas** diretamente do ambiente do aluno, utilizando autenticação e navegação automatizada via Selenium.

---

## ⚙️ Funcionalidades

- Login automático com matrícula e senha fornecidos pelo usuário;
- Navegação automatizada até o menu de **Agendamento de Provas**;
- Expansão dinâmica das disciplinas com provas corrigidas;
- Download e salvamento do HTML completo da correção da prova;
- Interface de menu navegável no terminal;
- Configuração inicial simples e persistente em `config.json`.

---

## 💻 Como usar (Windows)

### 1. Baixe o executável

Acesse a [página de releases](https://github.com/nicolasaigner/UVV-Toolkit/releases) do projeto e baixe o arquivo:

```
UVV_Toolkit_win_x86_64-vX.Y.Z.exe
```

---

### 2. Execute o programa

Clique duas vezes no executável ou rode pelo terminal/cmd:

```bash
UVV_Toolkit_win_x86_64-vX.Y.Z.exe
```

Na primeira execução, o programa solicitará:

- Matrícula UVV
- Senha UVV

Essas informações serão salvas em `config.json`, no mesmo diretório, e utilizadas automaticamente em execuções futuras.

---

### 3. Menu Interativo

Você verá um menu como este no terminal:

![UVV_CLI_Sequencia](https://github.com/user-attachments/assets/cefae4c8-2163-4a4f-a80b-247e0f3ab989)

Use as **teclas direcionais** **`↑`** e **`↓`** para navegar e pressione **`Enter`** para executar a opção selecionada.

> [!IMPORTANT]
> Quando finalizar, saia da aplicação, pois ela continua "escutando" o teclado.


Os arquivos das provas você verá em um pasta onde você executou o software, o nome da pasta será UVV_Materias e dentro tem as provas em `.html` e uma pasta `Content` com o `CSS` para deixar "bonitinha" a prova. 

Abra os arquivos `HTML` no navegador, caso queira exportar para PDF, utilize o `Imprimir` do seu navegador, geralmente, no Google Chorme é atalho `Ctrl + P`.

---

## 📂 Estrutura do Projeto

- `main.py`: Entrypoint. Controla o menu, configurações e fluxo principal.
- `menu.py`: Menu interativo com navegação via terminal.
- `busca_provas_corrigidas.py`: Implementa o scraping das provas corrigidas com Selenium.
- `build.py`: Script para gerar executável via PyInstaller.
- `uvv_toolkit.spec`: Configurações avançadas de build.
- `require-style.css`: Estilos utilizados no HTML salvo.
- `requirements.txt`: Dependências do projeto.

---

## 📦 Build (Somente desenvolvedores)

Se você deseja compilar este projeto localmente (Windows):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python build.py
```

O executável será gerado na pasta `dist/`.

---

## 🔒 Aviso

As credenciais são armazenadas localmente, sem criptografia. Use com responsabilidade.

---

## 🧑‍💻 Desenvolvedor

Nícolas Aigner
[GitHub](https://github.com/nicolasaigner) | [LinkedIn](https://linkedin.com/in/nicolasaigner/)

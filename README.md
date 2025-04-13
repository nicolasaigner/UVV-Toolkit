# UVV CLI Toolkit

**Versão:** v1.0.0  
**Plataforma suportada:** Windows (.exe)  
**Autor:** Nícolas

[![Build and Release UVV CLI Toolkit](https://github.com/nicolasaigner/UVV-Toolkit/actions/workflows/build-release.yml/badge.svg?branch=main)](https://github.com/nicolasaigner/UVV-Toolkit/actions/workflows/build-release.yml)
![Windows Downloads](https://img.shields.io/github/downloads/nicolasaigner/UVV-Toolkit/UVV_Toolkit_win_x86_64-v1.0.0.exe?label=Windows%20Downloads)
![ZIP Downloads](https://img.shields.io/github/nicolasaigner/UVV-Toolkit/archive/refs/tags/v1.0.0.zip?label=ZIP%20Downloads)
![TAR GZ Downloads](https://img.shields.io/github/nicolasaigner/UVV-Toolkit/archive/refs/tags/v1.0.0.tar.gz?label=TAR%20GZ%20Downloads)


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

```
==================================================
  UVV CLI Toolkit - v1.0.0
  Utilitário CLI para tarefas automatizadas do Portal UVV
==================================================

[>] Buscar Provas Corrigidas
[ ] Configurações do Usuário
[ ] Sair
```

Use as teclas direcionais para navegar e pressione `Enter` para executar a opção selecionada.

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

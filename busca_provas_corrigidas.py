# Código main.py completo com comentários em linha
import os
import re
import shutil
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# ========== AMBIENTE ==========
load_dotenv()
MATRICULA = os.getenv("UVV_MATRICULA")  # Matrícula do aluno (login)
SENHA = os.getenv("UVV_SENHA")  # Senha do aluno
RESET_DIR = os.getenv("UVV_RESET", "False").lower() == "true"  # Flag para resetar diretório
DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # Flag para realizar o debug no código

# Caminhos de diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "UVV_Materiais")
PROVA_DIR = os.path.join(DOWNLOAD_DIR, "Provas")
IMG_DIR = os.path.join(PROVA_DIR, "Content", "img")
CSS_DIR = os.path.join(PROVA_DIR, "Content", "css")

# Apagar diretório se estiver em modo RESET
if RESET_DIR and os.path.exists(DOWNLOAD_DIR):
    if DEBUG:
        print("[!] Resetando diretório de provas...")
    shutil.rmtree(DOWNLOAD_DIR)

# Criar diretórios necessários
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)

# ========== BAIXAR IMAGENS NECESSÁRIAS ==========
IMG_URLS = [
    "https://aluno.uvv.br/Content/img/tickMarckRed.png",
    "https://aluno.uvv.br/Content/img/tickMarckGreen.png"
]

for url in IMG_URLS:
    nome_img = url.split("/")[-1]
    caminho_img = os.path.join(IMG_DIR, nome_img)
    if not os.path.exists(caminho_img):
        r = requests.get(url)
        if r.status_code == 200:
            with open(caminho_img, "wb") as f:
                f.write(r.content)
            if DEBUG:
                print(f"[✔] Imagem baixada: {nome_img}")
        else:
            print(f"[!] Falha ao baixar imagem: {url}")

# ========== BAIXAR CSS EXTERNOS ==========
CSS_URLS = [
    "https://aluno.uvv.br/Content/css/bootstrap.min.css",
    "https://aluno.uvv.br/Content/css/font-awesome.min.css",
    "https://aluno.uvv.br/Content/css/estilo.css",
    "https://aluno.uvv.br/Content/css/app.css"
]

for url in CSS_URLS:
    nome_css = url.split("/")[-1]
    caminho_css = os.path.join(CSS_DIR, nome_css)
    if not os.path.exists(caminho_css):
        r = requests.get(url)
        if r.status_code == 200:
            with open(caminho_css, "wb") as f:
                f.write(r.content)
            if DEBUG:
                print(f"[✔] CSS baixado: {nome_css}")
        else:
            print(f"[!] Falha ao baixar CSS: {url}")

# ========== CSS CHECKBOX PADRÃO ==========
CUSTOM_CSS = """.form-inline .md-checkbox.md-checkbox-inline{margin-right:20px;top:3px}.md-checkbox input[type=checkbox]{visibility:hidden;position:absolute}.md-checkbox label{padding-left:30px;cursor:pointer}.md-checkbox label>span.inc{background:#fff;left:-20px;top:-20px;height:60px;width:60px;opacity:0;border-radius:50%!important;-moz-border-radius:50%!important;-webkit-border-radius:50%!important;-webkit-animation:.3s growCircle;-moz-animation:.3s growCircle;animation:.3s growCircle}.md-checkbox label>.box{top:0;border:2px solid #666;height:20px;width:20px;z-index:5;-webkit-transition-delay:0.2s;-moz-transition-delay:0.2s;transition-delay:0.2s}.md-checkbox input[type=checkbox]:checked~label>.box{opacity:0;-webkit-transform:scale(0) rotate(-180deg);-moz-transform:scale(0) rotate(-180deg);transform:scale(0) rotate(-180deg)}.md-checkbox input[type=checkbox]:disabled:checked~label>.check,.md-checkbox input[type=checkbox]:disabled~label,.md-checkbox input[type=checkbox]:disabled~label>.box,.md-checkbox input[type=checkbox][disabled]:checked~label>.check,.md-checkbox input[type=checkbox][disabled]~label,.md-checkbox input[type=checkbox][disabled]~label>.box{cursor:not-allowed;opacity:.7}.has-error .md-checkbox label,.has-error.md-checkbox label{color:#e73d4a}.has-error .md-checkbox label>.box,.has-error .md-checkbox label>.check,.has-error.md-checkbox label>.box,.has-error.md-checkbox label>.check{border-color:#e73d4a}.has-success .md-checkbox label>.box,.has-success .md-checkbox label>.check,.has-success.md-checkbox label>.box,.has-success.md-checkbox label>.check{border-color:#27a4b0}.md-checkbox input[type=checkbox]:checked~label>.check{opacity:1;-webkit-transform:scale(1) rotate(45deg);-moz-transform:scale(1) rotate(45deg);transform:scale(1) rotate(45deg)}.form-horizontal .md-checkbox-inline{margin-top:7px}.md-checkbox.md-checkbox-inline{display:inline-block}.md-checkbox-inline{margin:5px 0}.md-checkbox{position:relative}.md-checkbox label>.check{top:-4px;left:6px;width:10px;height:20px;border:2px solid #36c6d3;border-top:none;border-left:none;opacity:0;z-index:5;-webkit-transform:rotate(180deg);-moz-transform:rotate(180deg);transform:rotate(180deg);-webkit-transition-delay:0.3s;-moz-transition-delay:0.3s;transition-delay:0.3s}.md-checkbox label>span{display:block;position:absolute;left:0;-webkit-transition-duration:.3s;-moz-transition-duration:.3s;transition-duration:.3s}.md-checkbox input[type=checkbox]:disabled~label,.md-checkbox input[type=checkbox][disabled]~label{cursor:not-allowed}.has-success .md-checkbox label,.has-success.md-checkbox label{color:#27a4b0}label{font-weight:400}.panel .panel-body{font-size:13px}*{-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box}"""

with open(os.path.join(CSS_DIR, "custom-checkbox.css"), "w", encoding="utf-8") as f:
    f.write(CUSTOM_CSS)

# ========== CHROME ==========
options = Options()
options.add_argument("--start-maximized")
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# Inicializa driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ========== LOGIN ==========
driver.get("https://aluno.uvv.br/Login")
time.sleep(2)
print("[*] Realizando login...")
if DEBUG:
    print(f"[i] URL: \t\t{driver.current_url}")
    print(f"[i] Matricula: \t{MATRICULA}")
    print(f"[i] Senha: \t\t{SENHA}")
driver.find_element(By.ID, "Matricula").send_keys(MATRICULA)
driver.find_element(By.ID, "Password").send_keys(SENHA, Keys.RETURN)

# ========== AGENDAMENTO ==========
time.sleep(4)
driver.get("https://aluno.uvv.br/AgendamentoProva")
if DEBUG:
    print(f"[i] Acessando URL: {driver.current_url}")
time.sleep(4)
print("[*] Buscando provas com correção liberada...")

# ========== DETALHES ==========
while True:
    detalhes_spans = driver.find_elements(By.XPATH, '//span[contains(@ng-click, "exibirDetalhes")]')
    body = driver.find_element(By.TAG_NAME, "body")

    print(f"[*] Expandindo detalhes: {len(detalhes_spans)} detectados")

    driver.execute_script("arguments[0].scrollIntoView();", body)
    time.sleep(0.3)

    for span in detalhes_spans:
        try:
            driver.execute_script("arguments[0].click();", span)
            time.sleep(0.2)

            # faz um scroll suave para o elemento
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", span)
            time.sleep(0.3)

        except Exception as e:
            print(f"[!] Erro ao clicar no span de detalhes: {e}")

    rows = driver.find_elements(By.XPATH, '//tr[@ng-repeat="agenda in blog.agendamentos"]')
    print(f"[i] Verificando {len(rows)} linhas de agendamento...")

    encontrou = False

    for row in rows:
        try:
            # Busca pelo botão de correção <a> com o ng-click "visualizarCorrecao"
            correcao_btn = row.find_element(By.XPATH, './/a[contains(@ng-click, "visualizarCorrecao")]')
            # Pega a segunda coluna onde está com o header "Prova"
            nome_coluna = row.find_element(By.XPATH, './td[2]').text.strip()

            if DEBUG:
                # lista todas as colunas e imprime o valor da coluna
                col_val = row.find_elements(By.XPATH, './td')
                for i, coluna in enumerate(col_val):
                    print(f"Coluna {i}: {coluna.text.strip()}")

            # Verifica se a coluna contém " - "
            if " - " not in nome_coluna:
                continue

            # Separa o nome da prova e o nome da matéria
            prova_nome, materia_nome = nome_coluna.split(" - ", 1)
            # Remove espaços em branco extras
            prova_nome = prova_nome.strip()
            # Remove espaços em branco extras
            materia_nome = materia_nome.strip()
            # Pega a primeira coluna onde está com o header "Data da Prova" e remove espaços em branco extras
            data_da_prova = row.find_element(By.XPATH, './td[1]').text.strip()

            # Verifica se a data da prova contém "/" e/ou ":" e substitui por "-" e troca espaços por "_" ao mesmo tempo, com regex
            data_da_prova_sanitizada = re.sub(r"\s+-\s+", "-", re.sub(r"[/:]", "-", data_da_prova))

            # Sanitizar nome do arquivo fazendo substituições de caracteres especiais e espaços por "_"
            nome_arquivo = (
                    re.sub(r"[^a-zA-Z0-9_-]", "",
                           re.sub(r"\s+", "_",
                                  materia_nome.encode("ascii", "ignore").decode())
                           ) + "_" + data_da_prova_sanitizada + ".html")

            # Verifica se o nome do arquivo já existe
            caminho_saida = os.path.join(PROVA_DIR, nome_arquivo)

            # Verifica se o arquivo já existe
            if os.path.exists(caminho_saida):
                print(f"[-] Já existe: {nome_arquivo}, pulando...")
                continue

            # Verifica se o botão de correção está visível
            print(f"[+] Correção disponível: {materia_nome}")
            encontrou = True

            # Clica no botão de correção
            correcao_btn.click()
            time.sleep(2)

            # Utiliza o BeautifulSoup para fazer o parsing do HTML
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Seleciona o div que contém o conteúdo da prova
            div_conteudo = soup.select_one("div.conteudo.padding-conteudo.col-xs-12.col-md-12.col-sm-12.col-lg-12")

            # Verifica se o div foi encontrado
            if not div_conteudo:
                print(f"[!] Conteúdo não encontrado para: {materia_nome}")
                driver.back()
                time.sleep(2)
                break

            # Remove os elementos indesejados
            for img in div_conteudo.find_all("img"):

                # Verifica se a imagem contém "/Content/img/" e altera o src para o caminho local
                if img.has_attr("src") and "/Content/img/" in img["src"]:
                    nome_img = img["src"].split("/")[-1]
                    img["src"] = f"Content/img/{nome_img}"

            # Insere o CSS encontrados e baixados anteriormente
            styles = '<link rel="stylesheet" href="Content/css/bootstrap.min.css">\n'
            styles += '<link rel="stylesheet" href="Content/css/font-awesome.min.css">\n'
            styles += '<link rel="stylesheet" href="Content/css/estilo.css">\n'
            styles += '<link rel="stylesheet" href="Content/css/app.css">\n'

            # Adiciona o CSS customizado
            styles += '<link rel="stylesheet" href="Content/css/custom-checkbox.css">\n'

            # Adiciona título formatado na página HTML com a cor da letra branca
            titulo_html = f'<div style="margin-bottom: 20px; color: #fff;"><h2>{prova_nome} - {materia_nome} - {data_da_prova}</h2></div>'

            # Cria o HTML completo com o conteúdo da prova e o CSS
            html_final = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset=\"utf-8\">
    <title>{prova_nome} - {materia_nome} - {data_da_prova}</title>
    {styles}
</head>
<body>
{titulo_html}
{str(div_conteudo)}
</body>
</html>"""

            # Cria o arquivo HTML da prova com o HTML customizado
            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(html_final)

            print(f"[✔] Prova salva: {nome_arquivo}")

            # Volta para a página anterior
            driver.back()
            time.sleep(2)
            break

        except NoSuchElementException:
            continue
        except Exception as e:
            print(f"[!] Erro ao processar prova: {e}")

    if not encontrou:
        break

# ========== ENCERRAR ==========
driver.quit()
print("[✔] Finalizado.")

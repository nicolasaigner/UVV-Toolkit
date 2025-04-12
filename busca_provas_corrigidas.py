import os
import json
import re
import shutil
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def run():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
    CSS_FILE = os.path.join(BASE_DIR, "require-style.css")

    # ========== CONFIGURAÇÃO DO USUÁRIO ==========
    if not os.path.exists(CONFIG_FILE):
        print("[✘] Arquivo de configuração 'config.json' não encontrado!")
        exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    MATRICULA = config.get("matricula", "").strip()
    SENHA = config.get("senha", "").strip()
    RESET_DIR = config.get("reset", False)
    DEBUG = config.get("debug", False)

    if not MATRICULA or not SENHA:
        print("[✘] Matrícula ou senha não configuradas no 'config.json'!")
        exit(1)

    # ========== DIRETÓRIOS ==========
    DOWNLOAD_DIR = os.path.join(BASE_DIR, "UVV_Materiais")
    PROVA_DIR = os.path.join(DOWNLOAD_DIR, "Provas")
    IMG_DIR = os.path.join(PROVA_DIR, "Content", "img")
    CSS_DIR = os.path.join(PROVA_DIR, "Content", "css")

    if RESET_DIR and os.path.exists(DOWNLOAD_DIR):
        if DEBUG:
            print("[!] Resetando diretório UVV_Materiais...")
        shutil.rmtree(DOWNLOAD_DIR)

    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(CSS_DIR, exist_ok=True)

    # ========== DOWNLOAD IMAGENS ==========
    IMG_URLS = [
        "https://aluno.uvv.br/Content/img/tickMarckRed.png",
        "https://aluno.uvv.br/Content/img/tickMarckGreen.png"
    ]
    for url in IMG_URLS:
        nome = url.split("/")[-1]
        caminho = os.path.join(IMG_DIR, nome)
        if not os.path.exists(caminho):
            r = requests.get(url)
            if r.status_code == 200:
                with open(caminho, "wb") as f:
                    f.write(r.content)

    # ========== DOWNLOAD CSS ==========
    CSS_URLS = [
        "https://aluno.uvv.br/Content/css/bootstrap.min.css",
        "https://aluno.uvv.br/Content/css/font-awesome.min.css",
        "https://aluno.uvv.br/Content/css/estilo.css",
        "https://aluno.uvv.br/Content/css/app.css"
    ]
    for url in CSS_URLS:
        nome = url.split("/")[-1]
        caminho = os.path.join(CSS_DIR, nome)
        if not os.path.exists(caminho):
            r = requests.get(url)
            if r.status_code == 200:
                with open(caminho, "wb") as f:
                    f.write(r.content)

    # ========== CSS CUSTOMIZADO ==========
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        custom_css = f.read()

    with open(os.path.join(CSS_DIR, "custom-checkbox.css"), "w", encoding="utf-8") as f:
        f.write(custom_css)

    # ========== INICIAR SELENIUM ==========
    options = Options()
    options.add_argument("--start-maximized")
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # ========== LOGIN ==========
    driver.get("https://aluno.uvv.br/Login")
    time.sleep(2)
    driver.find_element(By.ID, "Matricula").send_keys(MATRICULA)
    driver.find_element(By.ID, "Password").send_keys(SENHA, Keys.RETURN)

    time.sleep(4)
    driver.get("https://aluno.uvv.br/AgendamentoProva")
    time.sleep(4)

    print("[*] Buscando provas com correção liberada...")

    while True:
        spans = driver.find_elements(By.XPATH, '//span[contains(@ng-click, "exibirDetalhes")]')
        if not spans:
            break

        for span in spans:
            try:
                driver.execute_script("arguments[0].click();", span)
                time.sleep(0.3)
            except Exception:
                continue

        rows = driver.find_elements(By.XPATH, '//tr[@ng-repeat="agenda in blog.agendamentos"]')
        encontrou = False

        for row in rows:
            try:
                correcao_btn = row.find_element(By.XPATH, './/a[contains(@ng-click, "visualizarCorrecao")]')

                data_prova = row.find_element(By.XPATH, './td[1]').text.strip()
                nome_coluna = row.find_element(By.XPATH, './td[2]').text.strip()

                if " - " not in nome_coluna:
                    continue

                prova_nome, materia_nome = nome_coluna.split(" - ", 1)
                prova_nome = prova_nome.strip()
                materia_nome = materia_nome.strip()

                data_sanitizada = re.sub(r"[/:]+", "-", re.sub(r"\s+", "", data_prova))

                nome_arquivo = (
                    re.sub(r"[^a-zA-Z0-9_-]", "",
                        re.sub(r"\s+", "_", materia_nome.encode("ascii", "ignore").decode()))
                    + "_-_" + data_sanitizada + ".html"
                )

                path_saida = os.path.join(PROVA_DIR, nome_arquivo)
                if os.path.exists(path_saida):
                    print(f"[-] Já existe: {nome_arquivo}, pulando...")
                    continue

                correcao_btn.click()
                time.sleep(2)

                soup = BeautifulSoup(driver.page_source, "html.parser")
                div = soup.select_one("div.conteudo.padding-conteudo.col-xs-12.col-md-12.col-sm-12.col-lg-12")
                if not div:
                    driver.back()
                    time.sleep(2)
                    break

                for img in div.find_all("img"):
                    if img.has_attr("src") and "/Content/img/" in img["src"]:
                        img["src"] = "Content/img/" + img["src"].split("/")[-1]

                styles = '\n'.join([
                    '<link rel="stylesheet" href="Content/css/bootstrap.min.css">',
                    '<link rel="stylesheet" href="Content/css/font-awesome.min.css">',
                    '<link rel="stylesheet" href="Content/css/estilo.css">',
                    '<link rel="stylesheet" href="Content/css/app.css">',
                    '<link rel="stylesheet" href="Content/css/custom-checkbox.css">'
                ])

                titulo_html = f'<div style="margin-bottom: 20px; color: #fff;"><h2>{prova_nome} - {materia_nome} - {data_prova}</h2></div>'

                html_final = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{prova_nome} - {materia_nome} - {data_prova}</title>
{styles}
</head>
<body>
{titulo_html}
{str(div)}
</body>
</html>"""

                with open(path_saida, "w", encoding="utf-8") as f:
                    f.write(html_final)

                print(f"[✔] Prova salva: {nome_arquivo}")
                driver.back()
                time.sleep(2)
                encontrou = True
                break

            except NoSuchElementException:
                continue
            except Exception as e:
                print(f"[!] Erro ao processar prova: {e}")

        if not encontrou:
            break

    driver.quit()
    print("[✔] Finalizado.")

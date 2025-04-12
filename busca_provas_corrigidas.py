import os
import sys
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
import traceback

# Configurar cache fora da pasta temporária do PyInstaller
if getattr(sys, 'frozen', False):
    WDM_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".uvv_webdriver_cache")
else:
    WDM_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webdriver_cache")

os.environ["WDM_CACHE_DIR"] = WDM_CACHE_DIR

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    EMBEDDED_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EMBEDDED_DIR = BASE_DIR

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
CSS_FILE = os.path.join(EMBEDDED_DIR, "require-style.css")

def run():


    # print(f"Caminho completo do arquivo de configuração: {os.path.abspath(CONFIG_FILE)}")
    # print(f"Caminho completo do arquivo de estilo CSS: {os.path.abspath(CSS_FILE)}")

    try:
        # ========== CONFIGURAÇÃO DO USUÁRIO ==========
        if not os.path.exists(CONFIG_FILE):
            print("[✘] Arquivo de configuração 'config.json' não encontrado!")
            input("Pressione Enter para voltar ao menu...")
            return

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)

        matricula: str = str(config.get("matricula", "")).strip()
        senha: str = config.get("senha", "").strip()
        reset_dir: bool = config.get("reset", False)
        debug: bool = config.get("debug", False)

        if not matricula or not senha:
            print("[✘] Matrícula ou senha não configuradas no 'config.json'!")
            input("Pressione Enter para voltar ao menu...")
            return

        # ========== DIRETÓRIOS ==========
        download_dir = os.path.join(BASE_DIR, "UVV_Materiais")
        prova_dir = os.path.join(download_dir, "Provas")
        img_dir = os.path.join(prova_dir, "Content", "img")
        css_dir = os.path.join(prova_dir, "Content", "css")

        if reset_dir and os.path.exists(download_dir):
            if debug:
                print("[!] Resetando diretório UVV_Materiais...")
            shutil.rmtree(download_dir)

        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(css_dir, exist_ok=True)

        # ========== DOWNLOAD IMAGENS ==========
        img_urls = [
            "https://aluno.uvv.br/Content/img/tickMarckRed.png",
            "https://aluno.uvv.br/Content/img/tickMarckGreen.png"
        ]
        for url in img_urls:
            nome = url.split("/")[-1]
            caminho = os.path.join(img_dir, nome)
            if not os.path.exists(caminho):
                r = requests.get(url)
                if r.status_code == 200:
                    with open(caminho, "wb") as f:
                        f.write(r.content)

        # ========== DOWNLOAD CSS ==========
        css_urls = [
            "https://aluno.uvv.br/Content/css/bootstrap.min.css",
            "https://aluno.uvv.br/Content/css/font-awesome.min.css",
            "https://aluno.uvv.br/Content/css/estilo.css",
            "https://aluno.uvv.br/Content/css/app.css"
        ]
        for url in css_urls:
            nome = url.split("/")[-1]
            caminho = os.path.join(css_dir, nome)
            if not os.path.exists(caminho):
                r = requests.get(url)
                if r.status_code == 200:
                    with open(caminho, "wb") as f:
                        f.write(r.content)

        # ========== CSS CUSTOMIZADO ==========
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            custom_css = f.read()

        with open(os.path.join(css_dir, "custom-checkbox.css"), "w", encoding="utf-8") as f:
            f.write(custom_css)

        # ========== INICIAR SELENIUM ==========
        options = Options()
        options.add_argument("--start-maximized")
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # ========== LOGIN ==========
        driver.get("https://aluno.uvv.br/Login")
        time.sleep(2)
        driver.find_element(By.ID, "Matricula").send_keys(matricula)
        driver.find_element(By.ID, "Password").send_keys(senha, Keys.RETURN)

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

                    path_saida = os.path.join(prova_dir, nome_arquivo)
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
    except Exception as e:
        print(f"[ERRO FATAL]: {e}")
        traceback.print_exc()
        input("Pressione Enter para sair...")

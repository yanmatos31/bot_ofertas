import pandas as pd
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Configuração do navegador Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Execução em modo headless (sem interface gráfica)
chrome_service = Service('path_to_chromedriver')  # Substitua 'path_to_chromedriver' pelo caminho para o chromedriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# URL do site que você deseja acessar
url = 'https://www.promobit.com.br'

# Navegar até a página principal
driver.get(url)

# Esperar até que os elementos das ofertas sejam carregados na página
wait = WebDriverWait(driver, 10)
offer_elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.flex.flex-col.rounded-2.bg-neutral-high-100.dark:bg-neutral-low-500.md:justify-between.lg:hover:shadow-md.lg:hover:transition-all.lg:hover:ease-in.h-full')))

# Pegar apenas os 10 primeiros elementos
offers = offer_elements[:20]

# Criar uma lista para armazenar os itens das ofertas
offers_data = []

# Iterar sobre as 10 primeiras ofertas e adicionando à lista
for offer in offers:
    link2_print = ''
    link_element = offer.find_element(By.CSS_SELECTOR, 'a.no-underline[&>*]:text-primary-400[&>*]:hover:text-primary-300[&>*]:active:text-primary-200[&>*]:dark:text-primary-200[&>*]:hover:dark:text-primary-100[&>*]:active:dark:text-primary-100.flex.h-full.flex-col.justify-between.rounded-2.border.border-neutral-high-300.dark:border-neutral-low-300.lg:border-none')
    link = link_element.get_attribute('href')

    # Se o link não for uma URL completa, construímos a URL completa
    if not link.startswith('http'):
        link = url + link

    # Navegar até a página da oferta
    driver.get(link)

    # Extraindo as informações de title e price
    title_element = driver.find_element(By.CSS_SELECTOR, 'h1.text-neutral-low-400.dark:text-neutral-high-200.font-sans.text-lg.font-bold.lg:text-2xl')
    title = title_element.text.strip()

    price_element = driver.find_element(By.CSS_SELECTOR, 'span.font-sans.text-2xl.font-bold.tracking-normal.lg:text-4xl.whitespace-nowrap.text-primary-500.dark:text-primary-100')
    price = price_element.text.strip()

    # Verificar se o link tem cupom
    link_element2 = driver.find_element(By.CSS_SELECTOR, 'a.flex.min-w-max.select-none.items-center.border-solid.justify-center.rounded-3.border.no-underline.transition-all.ease-in.w-full.p-4.min-h-10.text-base.border-success-300.bg-success-300.focus:ring-success-200.focus:outline-none.focus:ring-1.text-neutral-high-100[&>svg]:text-neutral-high-100.hover:border-success-500.hover:bg-success-500.hover:shadow-[0_1px_2px_0_rgba(19,19,19,0.4)]')
    if link_element2 is None:
        # Se não houver cupom, clicar para aparecer o pop-up
        link_element.click()
        link2_element = driver.find_element(By.CSS_SELECTOR, 'a.font-sans.whitespace-pre-wrap.mt-1.text-xs.text-neutral-low-100.dark:text-neutral-high-300.lg:text-sm')
        link2 = link2_element.get_attribute('href')
    else:
        link2 = link_element2.get_attribute('href')

    # Se houver link2, navegar até a página do link2
    if link2:
        driver.get(link2)
        link2_element = driver.find_element(By.CSS_SELECTOR, 'html>script:nth-child(3)')
        regex = r"'([^']*)'"
        link2_print = re.search(regex, link2_element.get_attribute('outerHTML')).group(1)

    # Montando a string para a coluna "Anúncio"
    anuncio = f'{title}\n\n' f'🔥 R$ {price}\n\n' f'💲 Compre aqui: {link2_print}'

    # Adicionando o item à lista de ofertas
    offers_data.append({'Título': title, 'Preço': price, 'Link': link2_print, 'Anúncio': anuncio})

# Criando o DataFrame a partir da lista de dicionários
df_offers = pd.DataFrame(offers_data)

# Salvando as ofertas em um arquivo Excel
excel_file_path = 'top_10_ofertas.xlsx'
df_offers.to
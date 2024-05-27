import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# URL do site que você deseja acessar
url = 'https://www.promobit.com.br'

# Fazendo uma solicitação HTTP para a página principal
response = requests.get(url)

# Verificando se a solicitação foi bem-sucedida (código 200)
if response.status_code == 200:
    # Criando um objeto BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrando e iterando sobre os elementos que atendem à condição desejada
    offer_elements = soup.find_all('div', class_='flex flex-col rounded-2 bg-neutral-high-100 dark:bg-neutral-low-500 md:justify-between lg:hover:shadow-md lg:hover:transition-all lg:hover:ease-in h-full')

    # Pegando apenas os 10 primeiros elementos
    offers = offer_elements[:20]

    # Criando uma lista para armazenar os itens das ofertas
    offers_data = []

    # Iterando sobre as 10 primeiras ofertas e adicionando à lista
    for offer in offers:
        link2 = ''
        link_element = offer.find('a', class_='no-underline [&>*]:text-primary-400 [&>*]:hover:text-primary-300 [&>*]:active:text-primary-200 [&>*]:dark:text-primary-200 [&>*]:hover:dark:text-primary-100 [&>*]:active:dark:text-primary-100 flex h-full flex-col justify-between rounded-2 border border-neutral-high-300 dark:border-neutral-low-300 lg:border-none')
        link = link_element['href'] if link_element and 'href' in link_element.attrs else ''

        # Se o link não for uma URL completa, construímos a URL completa
        if not link.startswith('http'):
            link = url + link

        # Fazendo uma solicitação HTTP para a página da oferta
        offer_response = requests.get(link)

        # Verificando se a solicitação foi bem-sucedida
        if offer_response.status_code == 200:
            # Criando um objeto BeautifulSoup para a página da oferta
            offer_soup = BeautifulSoup(offer_response.text, 'html.parser')

            # Extraindo as informações de title e price
            title_element = offer_soup.find('h1', class_='text-neutral-low-400 dark:text-neutral-high-200 font-sans text-lg font-bold lg:text-2xl')
            title = title_element.text.strip() if title_element else ''

            price_element = offer_soup.find('span', class_='font-sans text-2xl font-bold tracking-normal lg:text-4xl whitespace-nowrap text-primary-500 dark:text-primary-100')
            price = price_element.text.strip() if price_element else ''

            # Corrigindo o seletor de classe CSS para link2
            link_element2 = offer_soup.find('a', class_='flex min-w-max select-none items-center border-solid justify-center rounded-3 border no-underline transition-all ease-in w-full p-4 min-h-10 text-base border-success-300 bg-success-300 focus:ring-success-200 focus:outline-none focus:ring-1 text-neutral-high-100 [&>svg]:text-neutral-high-100 hover:border-success-500 hover:bg-success-500 hover:shadow-[0_1px_2px_0_rgba(19,19,19,0.4)]')
            
            # Teste se tem cupom no link
            print(link_element2)
            if link_element2 == None:
                 #clicar para aparecer o pop-up
                 link3 = offer_soup.find('a', class_='font-sans whitespace-pre-wrap mt-1 text-xs text-neutral-low-100 dark:text-neutral-high-300 lg:text-sm')
                 cupom_element = offer_soup.find('span', class_='flex items-center justify-center font-bold text-success-300 dark:text-success-400 p-2 text-2xl md:p-3')
                 cupom = cupom_element.text.strip() if cupom_element else ''
                 print(cupom)
                 link_element2 = offer_soup.find('a', class_='flex min-w-max select-none items-center border-solid justify-center rounded-2 border no-underline transition-all ease-in focus:border-primary-200 focus:outline-none visible w-full p-3 h-[50px] text-base border-success-300 bg-success-300 text-neutral-high-100 [&amp;>svg]:text-neutral-high-100 hover:border-success-400 hover:bg-success-400 mt-4')
                 link2 = link_element2['href'] if link_element2 and 'href' in link_element2.attrs else ''
            else:
                link2 = link_element2['href'] if link_element2 and 'href' in link_element2.attrs else ''



            # Fazendo uma solicitação HTTP para a página do link2
            if link2:
                offer_response2 = requests.get(link2)
                regex = r"'([^']*)'"
                if offer_response2.status_code == 200:
                    # Extraindo as informações de link2
                    link2_soup = BeautifulSoup(offer_response2.text, 'html.parser')
                    link_element2 = link2_soup.select_one('html>script:nth-child(3)')
                    #link_element2 = link2_soup.find('a', string='clique aqui.')
                    #link_element2 = link2_soup.find('body').find('div', class_='center').find('div').find('p').find('a')
                    #link2 = link_element2.get('href') if link_element2 and 'href' in link_element2.attrs else ''
                    link2 = re.search(regex, str(link_element2))
                    link2_print = link2.group(1)


            # Montando a string para a coluna "Anúncio"
            anuncio = f'{title}\n\n' f'🔥 R$ {price}\n\n' f'💲 Compre aqui: {link2_print}'

            # Adicionando o item à lista de ofertas
            offers_data.append({'Título': title, 'Preço': price, 'Link': link2_print, 'Anúncio': anuncio})

        else:
            print(f"Erro ao acessar a página da oferta. Código de status: {offer_response.status_code}")

    # Criando o DataFrame a partir da lista de dicionários
    df_offers = pd.DataFrame(offers_data)

    # Salvando as ofertas em um arquivo Excel
    excel_file_path = 'top_10_ofertas.xlsx'
    df_offers.to_excel(excel_file_path, index=False)

    print(f"Arquivo Excel gerado com sucesso: {excel_file_path}")


else:
    print(f"Erro ao acessar a página principal. Código de status: {response.status_code}")

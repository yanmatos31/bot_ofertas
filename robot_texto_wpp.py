from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import openpyxl
import os
import pyperclip

# Função para enviar mensagem via WhatsApp
def enviar_mensagem_whatsapp(contato, mensagem):
    # Configurações do Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=C:\Users\m1371121\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--profile-directory=Profile 1")
    #options.add_argument("--incognito")
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://web.whatsapp.com/")
    #input("Faça login no WhatsApp Web e pressione Enter depois que estiver logado...")

    time.sleep(10)  # Tempo para garantir que a página esteja completamente carregada

    # Localizar o campo de pesquisa
    search_box = driver.find_element("xpath", '//*[@aria-label="Caixa de texto de pesquisa"]')
    time.sleep(.5)
    search_box.click()
    search_box.send_keys(contato)
    search_box.send_keys(Keys.ENTER)

    time.sleep(2)  # Tempo para garantir que o chat esteja carregado

    # Localizar o campo de mensagem e enviar a mensagem
    message_box = driver.find_element("xpath", '//*[@aria-label="Digite uma mensagem"]')
    message_box.click()
    pyperclip.copy(mensagem)
    message_box.send_keys(Keys.CONTROL, 'v')
    time.sleep(10)
    message_box.send_keys(Keys.ENTER)

    time.sleep(2)  # Tempo para a mensagem ser enviada

    driver.quit()

# Caminho do arquivo Excel na área de trabalho
# desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
# excel_file = os.path.join(desktop_path, "lista_de_contatos.xlsx")
    
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
excel_file = os.path.join(script_dir, "top_10_ofertas.xlsx")

# Carregar o arquivo Excel
workbook = openpyxl.load_workbook(excel_file)
sheet = workbook.active
print(sheet)
# Iterar sobre as linhas do arquivo Excel e enviar mensagens
for row in sheet.iter_rows(min_row=2, values_only=True):
    numero_contato = str("Ofertas Net")
    mensagem = str(row[3])
    enviar_mensagem_whatsapp(numero_contato, mensagem)
    print("Mensagem enviada para:", numero_contato)

print("Todas as mensagens foram enviadas.")
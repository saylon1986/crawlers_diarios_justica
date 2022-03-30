# Imports de bibliotecas
import os
import pandas as pd
from requests.models import get_auth_from_url
from tqdm import tqdm
import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent
import urllib.request

# Imports Selenium (Navegador Web)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Chrome Driver
chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')
options = Options()
options.add_argument("--window-size=1920x1800")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
ua = UserAgent()


# Current Path 
dir_path = str(os.path.dirname(os.path.realpath(__file__)))
# print(dir_path)



def gerar_numeros():
	
	lista_num =[]
	inicio = 2095  # documento inicial disponível
	fim = 3001# documento final disponível

	atual = inicio
	for k in range(inicio, fim+1):
		lista_num.append(atual)
		atual = atual+1
	return lista_num	


def baixar_pdf(item,path):
	try:
		file = path + "\_doc_"+str(item)+".pdf"
		URL = "https://diario.tjba.jus.br/diario/internet/download.wsp?tmp.diario.nu_edicao=%d"%item
		response = urllib.request.urlopen(URL)    
		file = open(file, 'wb')
		file.write(response.read())
		file.close()
		return True
	except:
		return False	

numeracoes = gerar_numeros()
path = dir_path+'\Diarios_BA'
Path(path).mkdir(parents=True, exist_ok=True)

for item in numeracoes:
	while True:
		verif = baixar_pdf(item, path)
		if verif == True:
			break
			

driver.quit()
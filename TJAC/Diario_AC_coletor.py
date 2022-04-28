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
from PyPDF2 import PdfFileReader, PdfFileMerger
import shutil
import time
import datetime
from datetime import date
from workalendar.america import Brazil
import shutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import base64


######################  Função que verifica se os downloads acabaram #######################

def downloads_done(path_final):

	print()
	print("estamos verificando na pasta:", path_final)
	cont = 0
	desist = 0
	while True:
		if cont == 1 or desist == 4:  # contagem do documento ou das desistências
			break
		else:
			print("aguardando 15 seg")   # tempo de 15 segundos para cada tentativa
			print("-----")
			time.sleep(15)
			cont = 0
			total = os.listdir(path_final) #lista os casos no diretório
			
			if len(total) == 0: # se nada estiver em processo, cancelar.
				cont = 1
			else:
				for i in os.listdir(path_final):
					nome = str(i)
					if nome[-3:] == "pdf":  # verifica se o documento foi baixado
						cont = cont+1
						print("temos", cont, "arquivos baixados")
				desist = desist + 1

				print("Download em andamento. Aguarde")
				print("---------------")
					
	print("downloads finalizados")
	return


#########################################  Função que baixa os diários ##########################################

def Baixar_diarios(ano, datas, links):

	# cria o diretório caso não exista 

	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_AC_'+str(ano)
	Path(path).mkdir(parents=True, exist_ok=True)


	# itera pela data e o link (documento único)

	for data, link in zip(datas, links):

		# configurações do Chrome
		chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')
		
		# formata as datas
		data_pasta = data.replace("/","-")
		mes = data_pasta[4:6]

		# cria o diretório com o nome da data
		path_final = dir_path + f'\Diarios_AC_'+str(ano)+'\\'+data_pasta
		Path(path_final).mkdir(parents=True, exist_ok=True)
		
		# Configurações do Chrome driver
		options = Options()
		prefs = {'download.default_directory' : path_final}
		options.add_experimental_option('prefs', prefs)
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--window-size=1920x1800")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
		ua = UserAgent()

		# URL recebendo os elemento da data e o link
		link_final = 'https://diario.tjac.jus.br/edicoes.php?Ano='+str(ano)+'&Mes='+mes+'&PDF='+link
		

		# requisição do site 
		driver.get('https://diario.tjac.jus.br/edicoes.php?Ano='+str(ano)+'&Mes='+mes+'&PDF='+str(link))
		time.sleep(3)


		# verifica o download
		downloads_done(path_final)

		# encerra o processo
		driver.quit()




###########################  Função que converte os nomes dos diários no formato b64 que o site processa #######################

def Convert_names(datas):

	link_b64 = []
	for data in datas:
		data = data.strip()
		str_data = "/var/www/PDF/DE"+data+".pdf" # cria o link com a data
		# print(str_data)
		bites = bytes(str_data, encoding="utf-8") # converte a data para o formato B64
		# print(str(base64.b64encode(bites)))
		nome_doc = str(base64.b64encode(bites)) # tranforma o link em uma string
		link_b64.append(nome_doc[2:-1]) # salva na lista


	#retorna a lista	
	return link_b64	


#####################################################

def Gera_dias_uteis():

	# usuário escolhe as datas inicias e finais

	inicial = input("digite a data inicial(dd-mm-aaaa): ")
	final = input("digite a data final(dd-mm-aaaa): ")

	# converte as strings da data para o formato data

	data_inicial = datetime.strptime(inicial, '%d-%m-%Y').date()
	data_final = datetime.strptime(final, '%d-%m-%Y').date()
	

	date_list = pd.date_range(start= data_inicial, end = data_final) #gera a lista de datas
	# print(date_list)

	ano = int(date_list[0].strftime("%Y"))  # separa o ano

	# separa o calendário brasileiro as datas daquele ano
	cal = Brazil()
	cal.holidays(ano)


	# gera a lista de datas no formato necessário para o conversos b64 e para o link das URL e pastas
	datas = []
	datas_convert = []
	for item in date_list:
		ano = int(item.strftime("%Y"))
		mes = int(item.strftime("%m"))
		dia = int(item.strftime("%d"))
		if cal.is_working_day(date(ano,mes,dia)):
			data_str = str(item).replace("-","")[:9].strip()
			datas_convert.append(data_str)
			
			data = item.strftime("%d/%m/%Y")
			# print("date:",data)
			datas.append(data)


	return datas, datas_convert, ano


########################################## Chama as funções ###################

def Main():
	datas, datas_convert, ano = Gera_dias_uteis()
	links = Convert_names(datas_convert)
	Baixar_diarios(ano, datas, links)

#####################################################


Main()
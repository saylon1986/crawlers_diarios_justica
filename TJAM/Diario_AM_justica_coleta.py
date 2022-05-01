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




###############  Função que confere se os download terminaram ######################

def downloads_done(path_final):
	print()
	print("estamos verificando na pasta:", path_final)
	cont = 0
	desist = 0
	while True:
		if cont == 3 or desist == 4:  # limite de 3 documentos ou 4 tentativas
			break
		else:
			print("aguardando 15 seg") # 15 segundos para cada tentativa
			print("-----")
			time.sleep(15)
			cont = 0
			total = os.listdir(path_final) # lista os donwloads em andamento
			
			if len(total) == 0: # se nada estiver sendo baixado, cancela o processo.
				cont = 3
			else:
				for i in os.listdir(path_final):
					nome = str(i)
					if nome[-3:] == "pdf":  # confere os downloads finalizados
						cont = cont+1
						
				desist = desist + 1 # conta as tentativas

				print("Ainda falta(m)", 3-cont,"arquivos")
				print("---------------")
					
	print("downloads finalizados")
	return


##################################################################################

def Baixar_diarios(datas):


	# separa o ano e cria o diretório, caso não exista

	ano = str(datas[0][-4:])
	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_AM_'+ano
	Path(path).mkdir(parents=True, exist_ok=True)
    

    # indica os cadernos que serão baixados

	cadernos = ["2", "3", "4"]



	# para cada data, abre o Driver, cria o diretório com o nome do dia e faz o download de cada 
	
	for data in datas:
		chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')
		data_pasta = data.replace("/","-")
		path_final = dir_path + f'\Diarios_AM_'+ano+'\\'+data_pasta
		Path(path_final).mkdir(parents=True, exist_ok=True)

		## configurações do driver
		options = Options()
		prefs = {'download.default_directory' : path_final}
		options.add_experimental_option('prefs', prefs)
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--window-size=1920x1800")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
		ua = UserAgent()

		# URL para acessar os cadernos no site 
		driver.get("https://consultasaj.tjam.jus.br/cdje/index.do")
		WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="avancado"]/tbody/tr[5]/td[2]/table/tbody/tr/td/input[1]')))
		
		# para cada data, iterar em todos os cadernos
		for caderno in cadernos:
			driver.execute_script("popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s','cadernoDownload');"%(data, caderno))
			time.sleep(3)
		

		# verifica se o download acabou
		downloads_done(path_final)

		# fecha do driver
		driver.quit()
    


##################################   função que gera a lista de datas  #########################################

def Gera_dias_uteis():

	# usuário escolhe as datas inicias e finais

	inicial = input("digite a data inicial(dd-mm-aaaa): ")
	final = input("digite a data final(dd-mm-aaaa): ")

	# converte as strings da data para o formato data

	data_inicial = datetime.strptime(inicial, '%d-%m-%Y').date()
	data_final = datetime.strptime(final, '%d-%m-%Y').date()


	date_list = pd.date_range(start= data_inicial, end = data_final) # gera a lista de datas
	# print(date_list)

	ano = int(date_list[0].strftime("%Y")) # separa o ano escolhido pelo usuário
	
	# pacote que separa o calendário brasileiro e os feriados
	cal = Brazil()
	cal.holidays(ano)


	# separa as datas que são dias úteis no ano escolhido na formatação da URL

	datas = []
	for item in date_list:
		ano = int(item.strftime("%Y"))
		mes = int(item.strftime("%m"))
		dia = int(item.strftime("%d"))
		if cal.is_working_day(date(ano,mes,dia)):
			data = item.strftime("%d/%m/%Y")
			# print("date:",data)
			datas.append(data)


	return datas


######################################################

# Chama as funções

datas = Gera_dias_uteis()			
Baixar_diarios(datas)


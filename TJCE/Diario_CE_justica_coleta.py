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


#################  função que verifica se os downloads acabaram ####################

def downloads_done(path_final):

	print()
	print("estamos verificando na pasta:", path_final)
	cont = 0
	desist = 0
	while True:
		if cont == 1 or desist == 4: # controle da coleta ou da desistência
			break
		else:
			print("aguardando 15 seg") # tempo de 15 segundos
			print("-----")
			time.sleep(15)
			cont = 0
			total = os.listdir(path_final)
			
			if len(total) == 0: # desistência caso nada esteja sendo baixado
				cont = 1
			else:
				for i in os.listdir(path_final): # verifica os downloads em curso
					nome = str(i)
					if nome[-3:] == "pdf": # verifica os finalizados
						cont = cont+1 # controla a quantidade
						print("temos", cont, "arquivos baixados")
				desist = desist + 1 # controla as tentativas e o tempo

				print("Download em andamento. Aguarde")
				print("---------------")
					
	print("downloads finalizados")
	return


#############################################  Função que baixa os diários #####################################

def Baixar_diarios(datas):


	# formata o ano e cria o diretório
	ano = str(datas[0][-4:])
	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_CE_'+ano
	Path(path).mkdir(parents=True, exist_ok=True)


	# seleciona o caderno    
	cadernos = ["2"]

	
	# itera sobre cada data 
	for data in datas:

		# configurações do Chrome driver
		chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')

		#formata a data e cria o diretório
		data_pasta = data.replace("/","-")
		path_final = dir_path + f'\Diarios_CE_'+ano+'\\'+data_pasta
		Path(path_final).mkdir(parents=True, exist_ok=True)
		
		# configura o Chromedriver
		options = Options()
		prefs = {'download.default_directory' : path_final}
		options.add_experimental_option('prefs', prefs)
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--window-size=1920x1800")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
		ua = UserAgent()

		# acessa a URL principal
		driver.get("https://esaj.tjce.jus.br/cdje/index.do")
		WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="avancado"]/tbody/tr[5]/td[2]/table/tbody/tr/td/input[1]')))
		
		# itera sobre os cadernos
		for caderno in cadernos:
			driver.execute_script("popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s','cadernoDownload');"%(data, caderno))
			time.sleep(3)
		
		# verifica os downloads
		downloads_done(path_final)
		
		#fecha o driver
		driver.quit()
    


#####################################################

def Gera_dias_uteis():

	# usuário escolhe as datas inicias e finais

	inicial = input("digite a data inicial(dd-mm-aaaa): ")
	final = input("digite a data final(dd-mm-aaaa): ")

	# converte as strings da data para o formato data

	data_inicial = datetime.strptime(inicial, '%d-%m-%Y').date()
	data_final = datetime.strptime(final, '%d-%m-%Y').date()

	date_list = pd.date_range(start= data_inicial, end = data_final) # gera a lista de datas
	# print(date_list)

	ano = int(date_list[0].strftime("%Y")) #separa o ano
	

	# seleciona as datas do calendário brasileiro do ano
	cal = Brazil()
	cal.holidays(ano)


	# gera a lista de datas com os dias úteis
	datas = []
	for item in date_list:
		ano = int(item.strftime("%Y"))
		mes = int(item.strftime("%m"))
		dia = int(item.strftime("%d"))
		if cal.is_working_day(date(ano,mes,dia)):
			data = item.strftime("%d/%m/%Y")
			# print("date:",data)
			datas.append(data)

	# print(datas)
	return datas


######################################################

# chama as funções
datas = Gera_dias_uteis()			
Baixar_diarios(datas)


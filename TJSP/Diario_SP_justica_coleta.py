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


########################### Função que controla os downloads ############################

def downloads_done(path_final):
	print()
	print("estamos verificando na pasta:", path_final)
	cont = 0
	desist = 0
	while True:
		if cont == 5 or desist == 8: # controle da quantidade baixada e da desistência
			break
		else:
			print("aguardando 20 seg") # tempo de 20 seg
			print("-----")
			time.sleep(20)
			cont = 0
			total = os.listdir(path_final) # se nada estiver sendo baixado, cancela.
			if len(total) == 0:
				cont = 5
			else:
				for i in os.listdir(path_final): #lista os downnlods em curso
					nome = str(i)
					if nome[-3:] == "pdf": # verifica os concluídos
						cont = cont+1
				desist = desist + 1 # controla a desistência

				print("Ainda falta(m)", 5-cont,"arquivos")
				print("---------------")
					
	print("downloads finalizados")
	return


##################################################################################

def Baixar_diarios(datas):

	# formata o ano e cria o diretório

	ano = str(datas[0][-4:])
	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_SP_'+ano
	Path(path).mkdir(parents=True, exist_ok=True)
    

    # os cadernos a serem baixados
	cadernos = ["11", "12", "13", "15","18"]
	
	
	# itera sobre as datas
	for data in datas:

		# configuração do Chrome
		chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')
		
		# formata a data e cria o diretório
		data_pasta = data.replace("/","-")
		path_final = dir_path + f'\Diarios_SP_'+ano+'\\'+data_pasta
		Path(path_final).mkdir(parents=True, exist_ok=True)
		
		#configura o chrome
		options = Options()
		prefs = {'download.default_directory' : path_final}
		options.add_experimental_option('prefs', prefs)
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--window-size=1920x1800")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
		ua = UserAgent()


		# URL principal
		driver.get("https://www.dje.tjsp.jus.br/cdje/index.do")
		WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="avancado"]/tbody/tr[5]/td[2]/table/tbody/tr/td/input[1]')))
		
		# Para cada data, itera sobre os cadernos 
		for caderno in cadernos:
			driver.execute_script("popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s','cadernoDownload');"%(data, caderno))
			time.sleep(3)
		
		# controla o download
		downloads_done(path_final)
		
		#fecha o drive
		driver.quit()
    


######################################  Função que gera as datas   ##############################

def Gera_dias_uteis():

	data_inicial = input("digite a data inicial(mm-dd-aaaa): ") # data início
	data_final = input("digite a data final(mm-dd-aaaa): ") #data finam

	date_list = pd.date_range(start= data_inicial, end = data_final) #gera a lista de datas

	#gera o ano
	ano = int(date_list[0].strftime("%Y"))
	
	#seleciona o calendário brsileiro do ano
	cal = Brazil()
	cal.holidays(ano)


	# gerala  lista de datas com dias úteis
	datas = []
	for item in date_list:
		ano = int(item.strftime("%Y"))
		mes = int(item.strftime("%m"))
		dia = int(item.strftime("%d"))
		if cal.is_working_day(date(ano,mes,dia)):
			data = item.strftime("%d/%m/%Y")
			datas.append(data)

	return datas


######################################################

#chama as funções e inicia o processo
datas = Gera_dias_uteis()			
Baixar_diarios(datas)


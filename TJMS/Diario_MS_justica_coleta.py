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
from datetime import datetime



################### Função para verificar se os download acabaram ################# 

def downloads_done(path_final):
	
	print()
	print("estamos verificando na pasta:", path_final)

	cont = 0 # quantidade total de documentos
	desist = 0 # momento de desistência caso o site demore muito para responder
	
	while True:
		# se a desistência atingir a quantidade total + 2 elementos, ele desiste (ou seja, pelo menos 30s de tempo extra)
		# se a contagem identificar o mesmo número de item da quantidade total(2)

		if cont == 2 or desist == 4: 
			break # encerra o processo
		else:
			print("aguardando 15 seg")  # caso não seja ele aguarda 15 seg
			print("-----")
			time.sleep(15)
			cont = 0
			total = os.listdir(path_final) # faz a listagem da quantidade na pasta

			if len(total) == 0: # se depois de 15 seg ele verificar que não tem nada sendo baixado ele encerra o processo
				cont = 2
			else:
				for i in os.listdir(path_final):
					nome = str(i)
					
					if nome[-3:] == "pdf": # caso haja downloads em curso ele verifica se todos já estão completos (extensão ".pdf")
						cont = cont+1 # E conta quantos tem depois de iterar todos os elementos da pasta
						
				desist = desist + 1  # acrescenta 1 a desistência em cada verificação na pasta

				print("Ainda falta(m)", 2-cont,"arquivos") # indica para o usuário quantos ainda faltam
				print("---------------")
					
	print("downloads finalizados") # informa o encerramento do processo, acabado ou não.
	return



##################################################################################

def Baixar_diarios(datas):


	# cria o diretório com o nome do ano, caso não exista.	

	ano = str(datas[0][-4:])
	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_MS_'+ano
	Path(path).mkdir(parents=True, exist_ok=True)
    

    # Por default, baixamos apenas os cadernos 3 e 4
	cadernos = ["2","3"]

	
	for data in datas:

		# abre o driver
		chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')

		# cria a pasta com o nome da data, caso não existe
		data_pasta = data.replace("/","-")
		path_final = dir_path + f'\Diarios_MS_'+ano+'\\'+data_pasta
		Path(path_final).mkdir(parents=True, exist_ok=True)

		# configurações do Chrome para tamanho de tela, erros de certificado, driver e destino dos dowloads

		options = Options()
		prefs = {'download.default_directory' : path_final}
		options.add_experimental_option('prefs', prefs)
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--window-size=1920x1800")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
		ua = UserAgent()
		

		# URL que é iterada com as datas e os cadernos para baxar os diários
		driver.get("https://esaj.tjms.jus.br/cdje/index.do")
		WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="avancado"]/tbody/tr[5]/td[2]/table/tbody/tr/td/input[1]')))
		for caderno in cadernos:
			driver.execute_script("popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s'+'&amp;tpDownload=D','cadernoDownload');"%(data, caderno))
			time.sleep(3)
		

		# chama a função para verificar os andamentos dos downloads		
		downloads_done(path_final)

		# encerra a tela do Chrome
		driver.quit()
    


#####################################################

def Gera_dias_uteis():


	# usuário escolhe as datas inicias e finais

	inicial = input("digite a data inicial(dd-mm-aaaa): ")
	final = input("digite a data final(dd-mm-aaaa): ")

	# converte as strings da data para o formato data

	data_inicial = datetime.strptime(inicial, '%d-%m-%Y').date()
	data_final = datetime.strptime(final, '%d-%m-%Y').date()


	# gera a lista de datas

	date_list = pd.date_range(start= data_inicial, end = data_final)

	#separa o ano
	ano = int(date_list[0].strftime("%Y"))


	# Função que seleciona os dias úteis daquele ano no calendário brasileiro	
	cal = Brazil()
	cal.holidays(ano)

	# coloca as datas no formato adequado
	datas = []
	for item in date_list:
		ano = int(item.strftime("%Y"))
		mes = int(item.strftime("%m"))
		dia = int(item.strftime("%d"))
		if cal.is_working_day(date(ano,mes,dia)): # filtro dos dias úteis, excluindo os feriados
			data = item.strftime("%d/%m/%Y")
			# print("date:",data)
			datas.append(data)

	return datas


######################################################

# chama as funções para iniciar o processo

datas = Gera_dias_uteis()			
Baixar_diarios(datas)


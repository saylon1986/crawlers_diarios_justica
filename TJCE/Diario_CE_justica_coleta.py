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




def downloads_done(path_final):
	print()
	print("estamos verificando na pasta:", path_final)
	cont = 0
	desist = 0
	while True:
		if cont == 1:
			break
		else:
			print("aguardando 15 seg")
			print("-----")
			time.sleep(15)
			cont = 0
			for i in os.listdir(path_final):
				nome = str(i)
				if ".crdownload" not in nome:
					# print(i," finalizado")
					cont = cont+1
				else:
					print("Ainda falta 1 arquivo")
					print("---------------")
					desist = desist + 1
					if desist == 4:
						cont = 1
					
	print("downloads finalizados")
	return


##################################################################################

def Baixar_diarios(datas):


	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_CE_2021'
	Path(path).mkdir(parents=True, exist_ok=True)
    
	cadernos = ["2"]
	# datas = ["03/11/2021"]
	
	for data in datas:
		chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')
		data_pasta = data.replace("/","-")
		path_final = dir_path + f'\Diarios_CE_2021\\'+data_pasta
		Path(path_final).mkdir(parents=True, exist_ok=True)
		options = Options()
		prefs = {'download.default_directory' : path_final}
		options.add_experimental_option('prefs', prefs)
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--window-size=1920x1800")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
		ua = UserAgent()
		driver.get("https://esaj.tjce.jus.br/cdje/index.do")
		WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="avancado"]/tbody/tr[5]/td[2]/table/tbody/tr/td/input[1]')))
		for caderno in cadernos:
			driver.execute_script("popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s','cadernoDownload');"%(data, caderno))
			time.sleep(3)
		
		downloads_done(path_final)
		driver.quit()
    


#####################################################

def Gera_dias_uteis():

	data_inicial = input("digite a data inicial(mm-dd-aaaa): ")
	data_final = input("digite a data final(mm-dd-aaaa): ")

	date_list = pd.date_range(start= data_inicial, end = data_final)
	print(date_list)

	ano = int(date_list[0].strftime("%Y"))
	# print("o ano é", ano)
	
	cal = Brazil()
	cal.holidays(ano)

	datas = []
	for item in date_list:
		ano = int(item.strftime("%Y"))
		mes = int(item.strftime("%m"))
		dia = int(item.strftime("%d"))
		if cal.is_working_day(date(ano,mes,dia)):
			data = item.strftime("%d/%m/%Y")
			# print("date:",data)
			datas.append(data)

	print(datas)
	# z = input("")
	return datas


######################################################


datas = Gera_dias_uteis()			
Baixar_diarios(datas)


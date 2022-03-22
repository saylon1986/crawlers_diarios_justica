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




def downloads_done(path_final, quantidade):
	print()
	print("estamos verificando na pasta:", path_final)
	cont = 0
	desist = 0
	while True:
		if cont >= quantidade:
			break
		else:
			print("aguardando 15 seg")
			print("-----")
			time.sleep(15)
			cont = 0
			total = os.listdir(path_final)
			# print("temos", len(total), "arquivos nessa pasta")
			if len(total) == 0:
				cont = quantidade
			else:
				for i in os.listdir(path_final):
					nome = str(i)
					if ".crdownload" not in nome:
						# print(i," finalizado")
						cont = cont+1
						print("Ainda falta(m)", quantidade-cont,"arquivos")
						print("---------------")
						desist = desist + 1
						if desist == (quantidade+1):
							cont = quantidade
					
	print("downloads finalizados!")
	return


#########################################

def Baixar_diarios(ano, datas, links, quantidade = 1):


	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_AC_'+str(ano)
	Path(path).mkdir(parents=True, exist_ok=True)

	for data, link in zip(datas, links):
		chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')
		data_pasta = data.replace("/","-")
		mes = data_pasta[4:6]
		path_final = dir_path + f'\Diarios_AC_'+str(ano)+'\\'+data_pasta
		Path(path_final).mkdir(parents=True, exist_ok=True)
		options = Options()
		prefs = {'download.default_directory' : path_final}
		options.add_experimental_option('prefs', prefs)
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--window-size=1920x1800")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
		ua = UserAgent()
		link_final = 'https://diario.tjac.jus.br/edicoes.php?Ano='+str(ano)+'&Mes='+mes+'&PDF='+link
		# print(link_final) 
		driver.get('https://diario.tjac.jus.br/edicoes.php?Ano='+str(ano)+'&Mes='+mes+'&PDF='+str(link))
		time.sleep(3)

		downloads_done(path_final, quantidade)
		driver.quit()




######################################################

def Convert_names(datas):

	link_b64 = []
	for data in datas:
		data = data.strip()
		str_data = "/var/www/PDF/DE"+data+".pdf"
		# print(str_data)
		bites = bytes(str_data, encoding="utf-8")
		# print(str(base64.b64encode(bites)))
		nome_doc = str(base64.b64encode(bites))
		link_b64.append(nome_doc[2:-1])

	return link_b64	


#####################################################

def Gera_dias_uteis():

	data_inicial = input("digite a data inicial(mm-dd-aaaa): ")
	data_final = input("digite a data final(mm-dd-aaaa): ")

	date_list = pd.date_range(start= data_inicial, end = data_final)
	# print(date_list)

	ano = int(date_list[0].strftime("%Y"))
	# print("o ano é", ano)


	cal = Brazil()
	cal.holidays(ano)

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


	# print(datas)
	# print()
	# print(datas_convert)
	# z = input("")
	return datas, datas_convert, ano


######################################################

def Main():
	datas, datas_convert, ano = Gera_dias_uteis()
	links = Convert_names(datas_convert)
	Baixar_diarios(ano, datas, links)

#####################################################


Main()
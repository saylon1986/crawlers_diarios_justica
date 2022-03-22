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
from urllib import request
# Imports Selenium (Navegador Web)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfFileReader, PdfFileMerger
import shutil
import time
import datetime
from datetime import date
import shutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json



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



##########################################


def Baixar_diarios(ano, datas, cadernos, quantidade):


	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_MT_'+ano
	Path(path).mkdir(parents=True, exist_ok=True)
	print(datas)
	print()
	print(cadernos)


	chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')
	mes = str(datas[0][5:7])
	dia = str(datas[0][8:10])
	data = dia+"-"+mes+"-"+ano
	path_final = dir_path + f'\Diarios_MT_'+ano+'\\'+data
	Path(path_final).mkdir(parents=True, exist_ok=True)
	options = Options()
	prefs = {'download.default_directory' : path_final}
	options.add_experimental_option('prefs', prefs)
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--window-size=1920x1800")
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
	ua = UserAgent()
	# print()
	# print()
	# print()
	for nome in cadernos:
		nome = str(nome)
		if len(nome) > 5:
			print(nome)
			driver.get("https://dje-api.tjmt.jus.br/api/diarioOficial/documento/"+nome)
			time.sleep(3)

	downloads_done(path_final, quantidade)
	driver.quit()


#########################################


def ler_json(url):
	
	# url = "https://dje-api.tjmt.jus.br/api/diarioOficial/edicoes?periodoDataDe=2019-01-01T02:00:00.000Z&periodoDataAte=2019-12-31T03:00:00.000Z&indicePagina=0&quantidadePagina=242"
	html = request.urlopen(url).read()
	soup = BeautifulSoup(html,'html.parser')
	info = json.loads(soup.text)

	
	
	list_cadernos = []
	list_date_list = []
	list_quantidade = []

	# função que gera uma lista para cada data com seus respectivos cadernos após ler os JSON
	
	list_itens = info["items"]
	
	for n in list_itens:
		cadernos = []
		date_list = [] 
		list_docs = n["documentos"]
		for docs in list_docs:
			data = str(docs ["dataPublicacao"][:10])
			date_list.append(data)
			caderno = str(docs['enderecoPublicacao'])
			cadernos.append(caderno)
		list_cadernos.append(cadernos)
		list_date_list.append(date_list)
		quantidade = len(cadernos)
		list_quantidade.append(quantidade)

	# print(list_cadernos)
	# print(list_date_list)
	# print(list_quantidade)	
	return list_cadernos, list_date_list, list_quantidade

#############################################


def main():
	# para cada data iterar os cadernos
	anos_todos = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
	ano = input("digite o ano (ex: 2019): ")

	linha = anos_todos.index(ano)
	arq = open('URLS.txt', 'r')
	linhas = arq.readlines()
	url = linhas[linha]

	## ler a linha correspondente ao ano e enviar a url pra função json
	cadernos, date_lists, quantidades = ler_json(url)

	for caderno, date_list, quantidade in zip(cadernos, date_lists, quantidades):
		Baixar_diarios(ano, date_list, caderno, quantidade)


#############################################

main()
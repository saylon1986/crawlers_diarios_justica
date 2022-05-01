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




################### Função para verificar se os download acabaram ################# 

def downloads_done(path_final, quantidade):
	
	print()
	print("estamos verificando na pasta:", path_final)
	
	cont = 0 # quantidade total de documentos
	desist = 0 # momento de desistência caso o site demore muito para responder
	
	while True:
		if cont == quantidade: # se a contagem identificar o mesmo número de item da quantidade total
			break # encerra o processo
		
		else:
			print("aguardando 15 seg") # caso não seja ele aguarda 15 seg
			print("-----")
			time.sleep(15)
			cont = 0
			total = os.listdir(path_final) # faz a listagem da quantidade na pasta
			
			if len(total) == 0: 
				cont = quantidade # se depois de 15 seg ele verificar que não tem nada sendo baixado ele encerra o processo
			
			else:
				for i in os.listdir(path_final): # caso haja downloads em curso ele verifica se todos já estão completos (extensão ".pdf")
					nome = str(i)
					if nome[-3:] == "pdf": 
						cont = cont+1  # E conta quantos tem depois de iterar todos os elementos da pasta
	
				desist = desist + 1 # acrescenta 1 a desistência em cada verificação na pasta
				if desist == (quantidade+2): # se a desistência atingir a quantidade total + 2 elementos, ele desiste (ou seja, pelo menos 30s de tempo extra)
					cont = quantidade

				print("Ainda falta(m)", quantidade-cont,"arquivos") # indica para o usuário quantos ainda faltam
				print("---------------")

					
	print("downloads finalizados!") # informa o encerramento do processo, acabado ou não.
	return



##############################              Função para baixar os diários              #########################################


def Baixar_diarios(ano, datas, cadernos, quantidade):


	# cria o diretório com o nome do ano, caso não exista.	

	dir_path = str(os.path.dirname(os.path.realpath(__file__)))
	path = dir_path + f'\Diarios_MT_'+ano
	Path(path).mkdir(parents=True, exist_ok=True)


	# abre o driver

	chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver.exe')
	
	# ajsuta a data
	mes = str(datas[0][5:7])
	dia = str(datas[0][8:10])
	data = dia+"-"+mes+"-"+ano

	# cria a pasta com o nome da data, caso não existe
	
	path_final = dir_path + f'\Diarios_MT_'+ano+'\\'+data
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



	# usa a URL padrão para fazer o download dos cadernos com base no nome de cada um (os nomes no site são aleatórios!!)
	for nome in cadernos:
		nome = str(nome)
		if len(nome) > 5: # as vezes nas strings dos nomes vem algumas "sujeiras"
			# print(nome)
			driver.get("https://dje-api.tjmt.jus.br/api/diarioOficial/documento/"+nome)
			time.sleep(3)


	# chama a função para verificar os andamentos dos downloads		
	downloads_done(path_final, quantidade)

	# encerra a tela do Chrome
	driver.quit()


                           ################ Função para ler o JSON e coletar os nomes dos documentos para download ############## 


def ler_json(url):
															# exemplo de URL para registro
	# url = "https://dje-api.tjmt.jus.br/api/diarioOficial/edicoes?periodoDataDe=2019-01-01T02:00:00.000Z&periodoDataAte=2019-12-31T03:00:00.000Z&indicePagina=0&quantidadePagina=242"
	
	# faz a requisição na URL e guarda numa variável em formato JSON

	html = request.urlopen(url).read()
	soup = BeautifulSoup(html,'html.parser')
	info = json.loads(soup.text)

	
	## lista com os nomes dos cadernos

	list_cadernos = []
	list_date_list = []
	list_quantidade = []

	# função que gera uma lista para cada data com seus respectivos cadernos após ler os JSON
	
	list_itens = info["items"]
	
	# itera sobre essa lista no JSON coletando os nomes dos documentos, data de publicação e link 
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


	# retorna as listas
	return list_cadernos, list_date_list, list_quantidade



####################          Função principal              ######################


def main():

	# para cada data iterar os cadernos
	anos_todos = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
	ano = input("digite o ano (ex: 2019): ") # usuário escolhe o ano

	linha = anos_todos.index(ano)
	arq = open('URLS.txt', 'r') # abre a URL com os diários do ano escolhido pelo usuário no arquivo TXT
	linhas = arq.readlines()
	url = linhas[linha]

	## ler a linha correspondente ao ano e enviar a url pra função que faz a requisção do json
	cadernos, date_lists, quantidades = ler_json(url)


	# com as listas geradas pela função anterior, inicia o processo de downloads
	for caderno, date_list, quantidade in zip(cadernos, date_lists, quantidades):
		Baixar_diarios(ano, date_list, caderno, quantidade)


				#############################################



if __name__ == "__main__":
    main()
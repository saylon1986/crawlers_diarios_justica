import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import pandas as pd
from pathlib import Path



######################## função para gerar os números das edições de cada ano #################################

def gerar_numeros(ano):

    anos_todos = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
   
    linha = anos_todos.index(ano)
    arq = open('ANOS.txt', 'r') # abre o range das edições do ano escolhido pelo usuário no arquivo TXT
    linhas = arq.readlines() # lê o arquivo
    inic_fim = linhas[linha].split('-') # seleciona a linha do ano respectivo

    
    lista_num =[] #lista com os números do range do ano
    inicio = int(inic_fim[0])  # documento inicial disponível
    fim = int(inic_fim[1])# documento final disponível

    # gera o range do ano
    atual = inicio
    for k in range(inicio, fim+1):
        lista_num.append(atual)
        atual = atual+1

    # retorna a lista    
    return lista_num    



####################### função para coletar os documentos  #####################################################

def main():

    # usuário escolhe o ano
    ano = input("Digite o ano com 4 dígitos (Ex: 2019):")

    # gera o diretório do ano
    dir_path = str(os.path.dirname(os.path.realpath(__file__)))
    path = dir_path + f'\Diarios_BA_'+ano
    Path(path).mkdir(parents=True, exist_ok=True)


    # gera o range do ano
    edicoes = gerar_numeros(ano)

    for ed in edicoes:

        # gera a pasta da edição

        print("baixando edição", ed, ' de um total de', edicoes[-1],"\n-------------")
        path_final = dir_path + f'\Diarios_BA_'+ano+'\\'+str(ed)
        Path(path_final).mkdir(parents=True, exist_ok=True)
        

        # faz o request do site

        url = "https://diario.tjba.jus.br/diario/internet/pesquisar.wsp"
        session = requests.Session()
        r = session.get(url, verify=False) # Primeiro request para gerar um sessão válida.

        # Dicionário abaixo é os parâmetros para baixar o caderno:
        # - tmp.diario.nu_edicao: número da edição do diário;
        # - tmp.caderno: número do caderno;
        # - os outros parâmetros aparentemente não influenciam em muita coisa, porém é melhor não mexer.
        url_download = "https://diario.tjba.jus.br/diario/internet/download.wsp" # URL utilizada para baixar os cadernos.
        
        cadernos = [2,3,4]
        
        # itera para cada caderno salvando na pasta da edição
        for cad in cadernos:
            data = {'tmp.diario.nu_edicao': ed, 'tmp.caderno': cad, 'wi.page.prev': 'internet%2Farquivo', 'wi.token': ''}
            r = session.post(url_download, data=data, verify=False)
            filename = r.headers['Content-disposition'].split('filename=')[1].split("\"")[1] # Split do nome do arquivo.
         
            with open(path_final+"/"+filename, "wb") as f: # Escreve o conteúdo acessado para um arquivo.
                f.write(r.content)

######################################       ***     ###################################################


if __name__ == "__main__":
    warnings.simplefilter('ignore', InsecureRequestWarning) # Retira a exibição dos erros de SSL.
    main()


# TJMS


![Imagem do diario](image_diario_MS.png)


## Metodologia

#### 1. Coleta

Este sistema coleta os cadernos 2 e 3 do diário de justiça.

Para dar inicio ao processo é necessário inserir a data de início e de final.

##### Importante:

O formato da data a ser inserida é MÊS-DIA-ANO

Recomedamos selecionar o período de um ano por vez.

O algoritmo organiza os diários em pastas por ano e dentro delas, por pastas cujo nome é a data de cada diário.

#### 2. Parser


Para dar inicio ao processo é necessário inserir o ano da pasta a ser "parseada" no formato de 4 dígitos.

Este parser leva em consideração para realizar os recortes os blocos na forma como eles vem organizados no documentos,
já que nesse casos eles já estão organizados, em sua grande maioria, da forma correta.

Utilizando o python é possível acessar o texto na formato da sua estrutura gerando o seguinte resultado:

*{'number': 0, 'type': 0, 'bbox': (24.0, 361.0083312988281, 85.38816833496094, 368.7727966308594), 'lines': [{'spans': [{**'size': 6.949999809265137, 'flags': 16**, 'font': 'Arial,Bold', 'color': 0, 'ascender': 0.9052734375, 'descender': -0.2119140625, **'text': 'TRIBUNAL PLENO'**, 'origin': (24.0, 367.29998779296875), 'bbox': (24.0, 361.0083312988281, 85.38816833496094, 368.7727966308594)}], 'wmode': 0, 'dir': (1.0, 0.0), 'bbox': (24.0, 361.0083312988281, 85.38816833496094, 368.7727966308594)}]}*


Essa estrutura de um dicionario também é manuseada no python, do qual são extraídos os elementos indicados em negrito - *text, size* e *flag*. A escolha por manusear
esse elementos foi para filtrar, de saída, os textos que interessavam dos conteúdos desnecessários, como como indíces, caixas de texto de seções, cabeçalhos, etc.

O atributo *'text'* guarda o texto que visualizamos no PDF. O exemplo acima possui apenas um título, mas nas publicações temos uma série de spans com
inúmeras linhas de textos dentro delas.

Analisando os atributos *size* e *flag* mais frequentes nos diários desse tribunal, notamos a seguinte frequência: 

Index |  Tupla  | Quantidade |
----- | ------- |  --------  |
  1	  |*(8, 0)* | *3273322*  |
  2   |*(8, 16)*|   *49172*  |
  3   | (5, 0)  |    16147   |
  4   | (7, 0)  |     8325   |


 __(recortamos apenas o valor antes do ponto (.) e unimos um tupla com size e flag, respectivamente; organizando a frequência como descendente e escolhendo os 4 primeiros)__

Como se nota, destaca-se muito nos textos a tupla *size/flag* nos valores *7* e *0*. Isso indica que a maioria dos textos do diário possui essa configuração. Contudo, analisando as demais verificamos que em alguns casos raros, também as tuplas *10/0* e *7/16* também podem trazer informações do processo contendo textos que fazem parte da publicação.

A tupla 9/4 apenas traz alguns subtítulos e números das páginas.

Com base nesse estudo, foram selecionados dos diários apenas os textos com as formatações 1 e 2. Sendo que o padrão 2 são sempre as linhas com o número do processo nesse caso.

De posse dos textos das publicações o recorte atendeu ao seguinte critério:

1. Separamos a parte inicial da publicação - detalhes de como isso foi feito está no código
2. Buscamos o padrão CNJ nesse trecho do texto
3. Caso encontrado, salva a publicação e compara o número CNJ com o da publicação anterior(se houver).
	- Se os números forem iguais, unifica as publicações e elimina a última
	- Se forem diferentes, mantem as duas.
4. Caso ele não encontre o padrão CNJ no começo da publicação, ele unifica as publicações sem esse padrão com a anterior
até encontrar a próxima publicação com o padrão CNJ. Esse procedimento permite que uma publicação dividida em várias
seções seja unificada.


### Margem de erro:

Nos testes que realizamos tivemos os seguintes resultados:

1. Teste seguindo a ordem normal dos documentos:

- Quantidade de publicações:
- Quantidade verificada: 50 primeiras
- Erros e faltantes: 0
- Anos testados: 2019

2. Teste de amostra aleatória: (não realizado)

- Quantidade de publicações:
- Quantidade verificada: X primeiras
- Erros e faltantes: X
- Anos testados: 2019





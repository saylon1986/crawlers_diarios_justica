# TJBA 

![Imagem do diario](./image_diario_BA.png)


## Metodologia


#### 1. Coleta

Este sistema coleta os cadernos 2, 3 e 4 do diário de justiça. O caderno 1 foi eliminado por ser administrativo

O usuário deve escolher o ano para iniciar a coleta que, naturalmente, é feita pelo procedimento de um ano de cada vez.

O sistema gera o range das edições daquele ano e faz a iteração dos cadernos de cada edição, criando uma pasta com o nome da edição.


#### 2. Parser das publicações

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
  1	  |*(9, 0)* |   *42184*  |
  2   | (8, 0)  |     1208   |
  3   | (12, 18)|      445   |
  4   | (4, 4)  |       72   |


 __(recortamos apenas o valor antes do ponto (.) e unimos um tupla com size e flag, respectivamente; organizando a frequência como descendente e escolhendo os 4 primeiros)__

Como se nota, destaca-se muito nos textos a tupla *size/flag* nos valores *9* e *0*. Isso indica que a maioria dos textos do diário possui essa configuração. 

Com base nesse estudo e na verificação dos resultados, foram selecionados dos diários apenas os textos com a formatação 1.

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
- Quantidade verificada: X primeiras
- Erros e faltantes: X
- Anos testados: 2019

2. Teste de amostra aleatória:

- Quantidade de publicações:
- Quantidade verificada: X primeiras
- Erros e faltantes: X
- Anos testados: 2019

### Assunto e Comarca

O array de assuntos foram construídos de acordo com uma série de casos em que essa informação era facilmente identificável.

O módulo tanto dos assuntos quanto das comarcas retorna uma lista iterável. No caso so assuntos, cada item é testado na forma
de uma expressão regular. Por sua vez, a comarca é identificável pelo código presente dos 4 últimos dígitos do  número do
processo no padrão CNJ.
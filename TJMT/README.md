## TJMT - Metodologia

#### 1. Coleta

Este sistema coleta os cadernos do diário de justiçado Estado do Mato Grosso. Nesse site cada dia tem quantidades diferentes de cadernos,
além do link dos cadernos ser organizado pelo nome, que também não segue nenhum padrão.

Dessa forma, para encontrar os links (nomes dos cadernos de cada dia) foi necessário gerar uma requisição na página, que retorna uma URL em formato JSON
com todos os nomes dos cadernos de cada dia além de outras informações.

Com o nome de cada caderno o algoritmo faz o download dos arquivos em uma URL padrão. 

Por default essa URL foi dividida por anos, contendo todos os diários daquele ano dividio em dias.

Essas URLs estão em um documento TXT à parte do código e são selecionadas quando o usuário escolhe o ano.

Assim, para dar inicio ao processo é necessário inserir o ano a ser coletado.

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


#####   Tupla        Quantidade 

1 **(7, 0)       1510709** 
2   (7, 16)      157644 
3 **(9, 4)       25252** 
4 **(10, 0)      3500** 

__(recortamos apenas o valor antes do ponto (.) e unimos um tupla com size e flag, respectivamente; organizando a frequência como descendente e escolhendo os 4 primeiros)__

Como se nota, destaca-se muito nos textos a tupla *size/flag* nos valores *7* e *0*. Isso indica que a maioria dos textos do diário possui essa configuração. Contudo, analisando as demais verificamos que em alguns casos raros, também as tuplas *10/0* e *7/16* também podem trazer informações do processo contendo textos que fazem parte da publicação.

A tupla 9/4 apenas traz alguns subtítulos e números das páginas.

Com base nesse estudo, foram selecionados dos diários apenas os textos com as formatações 1, 3 e 4.

De posse dos textos das publicações o recorte atendeu ao seguinte critério:

1. Separamos a parte inicial da publicação - detalhes de como isso foi feito está no código
2. Buscamos o padrão CNJ nesse trecho do texto
3. Caso encontrado, salva a publicação e compara o número CNJ com o da publicação anterior(se houver).
	- Se os números forem iguais, unifica as publicações e elimina a última
	- Se forem diferentes, mantem as duas´.
4. Caso ele não encontre o padrão CNJ no começo da publicação, ele unifica as publicações sem esse padrão com a anterior
até encontrar a próxima publicação com o padrão CNJ. Esse procedimento permite que uma publicação dividida em várias
seções seja unificada.


### Margem de erro:

Nos testes que realizamos tivemos os seguintes resultados:

1. Teste seguindo a ordem normal dos documentos:

- Quantidade de publicações:
- Quantidade verificada: X primeiras
- Erros e faltantes: X


2. Teste de amostra aleatória:

- Quantidade de publicações:
- Quantidade verificada: X primeiras
- Erros e faltantes: X



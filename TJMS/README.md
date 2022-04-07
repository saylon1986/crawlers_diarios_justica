### TJMS - Metodologia

#### 1. Coleta

Este sistema coleta os cadernos 2 e 3 do diário de justiça.

Para dar inicio ao processo é necessário inserir a data de início e de final.

##### Importante:

O formato da data a ser inserida é MÊS-DIA-ANO

Recomedamos selecionar o período de um ano por vez.

O algoritmo organiza os diários em pastas por ano e dentro delas, por pastas cujo nome é a data de cada diário.

#### 2. Parser


Para dar inicio ao processo é necessário inserir o ano da pasta a ser "parseada".

Este parser leva em consideração para realizar os recortes os blocos na forma como eles vem organizados no documentos,
já que nesse casos eles já estão organizados, em sua grande maioria, da forma correta.


Contudo, muitas seções do documento trazem publicações que não são úteis, porque não tratam de processos judiciais, mas de questões administrativas.

Exemplos:


'Ata de distribuição de processos, elaborada em vinte e oito de fevereiro de dois mil dezenove pelo sistema de processamento  de dados da Secretaria do Tribunal de Justiça:'



Por esta razão, o critério adotado para selecionar as publicações que tratassem de decisões judiciais foi conter, no corpo do texto, ao menos uma numeração no padrão CNJ.

Há algumas publicações em que cada linha é fragmentada em uma seção ou, ainda, publicações em que parte do texto está na página seguinte. Nesses casos foi adotado o procedimento abaixo.


#### Publicações que excedem mais de uma página ou mais de uma seção:

Como há uma parcela das publicações que não é uniforme, o procedimento adotado foi o seguinte:
1. Realizar o teste de encontrar o número CNJ, 
2. Caso não encontrar, unificar o anterior (caso não seja o primeiro) até a quarta seção seguinte sem encontrar o número CNJ.
	Essa escolha foi feita depois de observar que até 4 seções posteriores a publicação com a numeração, pertenciam a ela.
	Em muitos casos há a soma de um pequeno trecho inadequado, mas a margem de erro observada foi bem pequena; o que justifica a adoção do método.






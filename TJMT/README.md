### TJMT - Metodologia

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

Para dar inicio ao processo é necessário inserir o ano da pasta a ser "parseada".

Este parser leva em consideração para realizar os recortes os blocos na forma como eles vem organizados no documentos,
já que nesse casos eles já estão organizados, em sua grande maioria, da forma correta.


Contudo, muitas seções do documento trazem publicações que não são úteis, porque não tratam de processos judiciais, mas de questões administrativas.

Exemplos:

"DEPARTAMENTO DO TRIBUNAL PLENO   ADMINISTRATIVO   PUBLICAÇÃO DE CONCLUSÃO DE JULGAMENTO       1 – PROPOSIÇÃO nº 26/2014 – DEPARTAMENTO DO TRIBUNAL PLENO  – N. 0173072-60.2014.8.11.0000  Relator: Des. Orlando de Almeida Perri   Decisão: "PROPOSTA DE ALTERAÇÃO DE EMENDA REGIMENTAL  APROVADA, POR UNANIMIDADE."   ***********   2 – PROPOSIÇÃO nº 27/2014 – DEPARTAMENTO DO TRIBUNAL PLENO  – N. 0173073-45.2014.8.11.0000 Relator: Des. Orlando de Almeida Perri   Decisão: "POR UNANIMIDADE APROVOU A MINUTA DE PROJETO DE  LEI  QUE  REGULAMENTA  A  JORNADA  DE  TRABALHO  DOS  SERVIDORES."   ***********   3 –  PEDIDO  DE  PROVIDÊNCIAS  nº  7/2014 –  DEPARTAMENTO  DE  CADASTRO DE MAGISTRADOS – N. 0173927-39.2014.8.11.0000 Relator: Des. Orlando de Almeida Perri   Decisão: "POR UNANIMIDADE APROVOU A ESCALA DE PLANTÃO  APRESENTADA."   ***********   Departamento do Tribunal Pleno em Cuiabá, aos 19 dias do mês de  dezembro de 2014.   Belª. MARIA CONCEIÇÃO BARBOSA CORRÊA Diretora do Departamento do Tribunal Pleno"


"ATO N. 862/2014/CMAG         O PRESIDENTE DO TRIBUNAL DE JUSTIÇA DO ESTADO DE MATO  GROSSO , no uso de suas atribuições legais, com base no artigo 96, I, "c"  da Constituição Federal e tendo em vista a decisão proferida pelo Tribunal  Pleno em sessão ordinária, realizada em 18-12-2014,     * O Ato nº 862/2014/CMAG completa encontra-se no Caderno de  Anexo do Diário da Justiça Eletrônico no final desta Edição."



Por esta razão, o critério adotado para selecionar as publicações que tratassem de decisões judiciais foi conter, no corpo do texto, ao menos uma numeração no padrão CNJ.

Há algumas publicações em que cada linha é fragmentada em uma seção ou, ainda, publicações em que parte do texto está na página seguinte. Nesses casos foi adotado o procedimento abaixo.


#### Publicações que excedem mais de uma página ou mais de uma seção:

Como há uma parcela das publicações que não é uniforme, o procedimento adotado doi o seguinte:
1. Realizar o teste de encontrar o número CNJ, 
2. Caso não encontrar, unificar o anterior (caso não seja o primeiro) até a quarta seção seguinte sem encontrar o número CNJ.
	Essa escolha foi feita depois de observar que até 4 seções posteriores a publicação com a numeração, pertenciam a ela.
	Em muitos casos há a soma de um pequeno trecho inadequado, mas a margem de erro observada foi bem pequena; o que justifica a adoção do método.




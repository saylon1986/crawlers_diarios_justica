### TJBA - Metodologia

#### 1. Coleta

Este sistema coleta o caderno completo do diário de justiça.
Por default o sistema já coleta os diários com numeração entre os anos de 2012 e 2021



#### 2. Parser


Este parser leva em consideração para realizar os recortes as posições dos elementos no texto, o tamanho e 
a flag; tendo como norte as posições mais frequentes dos parágrafos, que nesse caso é 42.

As linhas são unificadas em bloco de acordo com a organização do próprio texto, servindo estes de marcadores
de início e fim.



#### Ajustes:

1. Na coleta: tentar eliminar a parte administrativa do diário e coletar o diário em partess

2. No Parser:

O procedimento acima resolveu boa parte dos problemas de recorte, mas ainda temos casos em que as seções
unificam muitos parágrafos quebrados, sobretudo quando são páginas seguidas;	 gerando situações como a mostrada abaixo:

Classe : Mandado de Segurança nº 0017863-61.2017.8.05.0000 Foro de Origem : Salvador Órgão : Tribunal Pleno Relator : Des. Ivanilton Santos da Silva Impetrante : Concic Engenharia S/A Advogado : Francisco José Bastos (OAB: 4281/BA) Advogado : Solon Augusto Kelman de Lima (OAB: 11990/BA) Advogado : Larissa Ferreira Simões de Oliveira (OAB: 21513/BA) Impetrado : Presidente do Tribunal de Justiça da Bahia Impetrada : Juíza do Núcleo Auxiliar de Conciliação de Precatórios - NACP
-----------------

Trata-se de Mandado de Segurança, impetrado por COCIC ENGENHARIA S/A, contra ato dito coator do EXMO. DESEMBARGADOR PRESIDENTE DO TRIBUNAL DE JUSTIÇA DO ESTADO DA BAHIA, e da EXMA. JUÍZA ASSESSORA, RESPONSÁVEL PELO NÚCLEO AUXILIAR DE CONCILIAÇÃO DE PRECATÓRIOS - NACP, consubstanciado em adaptação a comando judicial transitado em julgado, encaminhado para cumprimento no Núcleo de Precatórios.
-----------------

Do compulsar dos fólios, averíguo não constar no writ qualquer pedido de antecipação de tutela, sendo assim, converto o julgamento em diligência para determinar à Secretaria deste Tribunal Pleno que notifique as autoridades coatoras acerca do conteúdo da petição inicial, enviando-lhes as vias apresentadas com as cópias dos documentos colacionados, para, no prazo de 10 (dez) dias, prestarem as informações que entenderem necessárias.
-----------------

Intime-se, pessoalmente, o representante judicial do Estado da Bahia, enviando-lhe cópia da inicial sem documentos, para que, querendo, intervenha no feito, conforme disposto no inciso II do art. 7º da Lei nº 12.016/09.


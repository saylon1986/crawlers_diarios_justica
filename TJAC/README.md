### TJAC - Metodologia

#### 1. Coleta

Este sistema coleta o caderno do diário de justiça.

Para dar inicio ao processo é necessário inserir a data de início e de final.

##### Importante:

O formato da data a ser inserida é MÊS-DIA-ANO

Recomedamos selecionar o período de um ano por vez.

Pelas características do site é preciso converter o número do link para um encode b64 e 
depois utilizar esse link na URL principal.


#### 2. Parser


Este parser leva em consideração para realizar os recortes os elementos no texto. Os
critério são os tamanho 8 e a flag 0. 




#### Ajustes:

O procedimento acima resolveu boa parte dos problemas de recorte, mas ainda temos casos em que as seções
unificam muitos parágrafos quebrados e publicações que excedem uma página, gerando situações como a mostrada abaixo:




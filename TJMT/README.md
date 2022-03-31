### TJMT - Metodologia

#### 1. Coleta

Este sistema coleta os cadernos do diário de justiça. Nesse sistema cada dia tem quantidades diferentes de cadernos,
além do link dos cadernos ser organizado pelo nome, que também não segue nenhum padrão.
Dessa forma, para encontrar os links foi necessário gerar uma requisição na página que retorna uma URL em formato JSON
com todos os nomes dos cadernos de cada dia.
Com o nome de cada caderno o algoritmo faz o download dos arquivos. 
Por default essa URL foi dividida por anos, contendo todos os diários daquele ano dividio em dias.
Essas URL estão em um documento TXT a parte do código e são selecionadas quando o usuário escolhe o ano.
Assim, para dar inicio ao processo é necessário inserir o ano a ser coletado.


#### 2. Parser


Este parser leva em consideração para realizar os recortes os blocos na forma como eles vem organizados no documentos,
Já que nesse casos eles já estão organizados da forma correta.



#### Ajustes:

1. No Parser: publicações que excedem mais de uma página




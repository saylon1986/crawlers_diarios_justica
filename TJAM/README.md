### TJAM - Metodologia

#### 1. Coleta

Este sistema coleta os cadernos 3,4 e 5 do diário de justiça.

Para dar inicio ao processo é necessário inserir a data de início e de final.

##### Importante:

O formato da data a ser inserida é MÊS-DIA-ANO

Recomedamos selecionar o período de um ano por vez.


#### 2. Parser


Este parser leva em consideração para realizar os recortes as posições dos elementos no texto, 
tendo como norte as posições mais frequentes dos parágrafos, que são 70, 316 e 317.

As linhas são unificadas em bloco de acordo com os valores dos parágrafos, servindo estes de marcadores
de início e fim.

Caso haja vários parágrafos consecutivos na lista, eles são unificados juntos.



#### Ajustes:

O procedimento acima resolveu boa parte dos problemas de recorte, mas ainda temos casos em que as seções
unificam muitos parágrafos quebrados, gerando situações como a mostrada abaixo:


------------------------
Conclusão de Acórdãos Processo: 0210980-41.2018.8.04.0022 - Correição Extraordinária,  Juiz Corregedor Auxiliar - Setor 2

------------------------
Corrigente: Exmo. Sr. Corregedor Geral de Justiça do Estado do Amazonas

------------------------
Presidente:  Yedo Simões de Oliveira. Relator:  Djalma Martins da Costa. Revisor:  Revisor do processo Não informado

------------------------
EMENTA: RELATÓRIO DE CORREIÇÃO EXTRAORDINÁRIA REALIZADA NA VARA 1.ª VARA DA COMARCA DE TEFÉ. HOMOLOGAÇÃO- A presente Correição extraordinária merece ser homologada,  porquanto reﬂ ete com ﬁ delidade os fatos narrados em sua missão, além de ter realizado minucioso trabalho nos autos dos processos examinados, livros e documentos existentes no Cartório da 1.ª Vara da Comarca de Tefé, consoante as formalidades legais exigidas;- Quanto à recomendações feitas, tenho-as como adequadas ao resultado da inspeção, merecendo destaque as que objetivam o aperfeiçoamento das condições físicas do Fórum de Justiça da Comarca de Tefé, bem como a designação de juízes, com exclusividade, e servidores para atuarem nas respectivas unidades judiciárias da referida Comarca, Publicação Oﬁ cial do Tribunal de Justiça do Estado do Amazonas - Lei Federal nº 11.419/06, art. 4º Disponibilização: quinta-feira, 7 de março de 2019 Diário da Justiça Eletrônico - Caderno Judiciário - Capital Manaus, Ano XI - Edição 2568 3 motivo porque acolho todas as recomendações sugeridas. - Relatório aprovado e homologado. .  DECISÃO: “Por unanimidade, o Egrégio Tribunal Pleno decidiu aprovar e homologar a Correição Extraordinária realizada no Cartório da 1.ª Vara da Comarca de Tefé, observadas as formalidades legais pertinentes à espécie, nos termos do voto do Reltor.”.  Sessão: 12 de fevereiro de 2019.


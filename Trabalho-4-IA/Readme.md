Trabalho 2 - Busca com Adversário

Alunos:

Ana Luíza Colombi Sanfelice (577504)

Lorenzo Cadó Nemitz (584809)

Natan Feijó Tristão (585193)

2.2 
A)

i)   Sim, o minimax sempre empata ou vence de randomplayer;

ii)  Sim, o minimax sempre empata entre si;

iii) O minimax no pior dos casos empata ao jogar contra humanos;

B)

Contagem de peças X Valor posicional: 35 x 29

Valor posicional X Contagem de peças: 40 x 20

Contagem de peças X Heurística customizada: 22 x 42

Heurística customizada X Contagem de peças: 59 x 5

Valor posicional X Heurística customizada: 19 x 45

Heurística customizada X Valor posicional: 49 x 15


A Heurística com mais vitória foi a custom, com um total de 4 vitórias e uma média de 48,75 peças por jogo.

A Contagem de Peças e a Valor posicional ganham entre si dependendo de qual começa jogando. 

Explicação da Heurística Customizada:

A heurística é uma combinação ponderada de várias medidas, com pesos adaptativos conforme fase do jogo. Os componentes combinados procuram balancear valorização de indicadores posicionais, por exemplo, cantos, mobilidade (quantidade de jogadas possíveis), além da diferença de peças. Ela é baseada na mask, levando em conta o número possível de jogadas para otimizar o max_depth da busca. 

A heurística foi baseada em discussões do grupo e ajudas da Inteligência Artifical "ChatGPT". Ela é classificada como uma Função de Avaliação Heurística Linear Ponderada por Fases.


3 
A heurística escolhida para o torneio será baseada em minimax, usando a versão custom, visto que ela tem uma boa performance comparada às propostas no trabalho.

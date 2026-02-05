from typing import Set, Tuple
import heapq
from itertools import count

OBJETIVO = "12345678_"

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado:str, pai:None, acao:str, custo:int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        # substitua a linha abaixo pelo seu codigo
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
    
    def __eq__(self, other):
        if not isinstance(other, Nodo):
            return NotImplemented
        return self.estado == other.estado
    
    def __hash__(self):
        return hash(self.estado)
    


def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    entrada =  list(estado) #transforma a string em lista
    indice = entrada.index('_') #encontra o índice do espaço vazio
    linha, coluna = divmod(indice, 3)

    def troca (i: int, j: int) -> str:
        nova_entrada = entrada.copy()
        nova_entrada[i], nova_entrada[j] = nova_entrada[j], nova_entrada[i]
        return ''.join(nova_entrada)

    resultado: Set[Tuple[str, str]] = set()

    if coluna > 0:
        resultado.add(("esquerda", troca(indice, indice - 1)))
    
    if linha < 2:
        resultado.add(("abaixo", troca(indice, indice + 3)))

    if coluna < 2:
        resultado.add(("direita", troca(indice, indice + 1)))

    if linha > 0:
         resultado.add(("acima", troca(indice, indice - 3)))
    
    return resultado


def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    sucessores = sucessor(nodo.estado)  # chama a função sucessor(estado)
    conjunto_nodos = set()

    for acao, novo_estado in sucessores:
        novo_nodo = Nodo(
            estado=novo_estado,
            pai=nodo,
            acao=acao,
            custo=nodo.custo + 1
        )
        conjunto_nodos.add(novo_nodo)

    return conjunto_nodos

def h_hamming(estado: str) -> int:
    """
    Calcula a distância de Hamming (número de peças fora do lugar)
    entre o estado atual e o estado objetivo ("12345678_").
    O espaço vazio '_' não é contado.
    """
    dist = 0
    for i in range(len(estado)):
        # Não conta o espaço vazio '_'
        if estado[i] != '_' and estado[i] != OBJETIVO[i]:
            dist += 1
    return dist

def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    if estado == OBJETIVO:
        return []

    seq = [c for c in estado if c != '_']
    inversions = sum(1 for i in range(len(seq)) for j in range(i+1, len(seq)) if seq[i] > seq[j])
    if inversions % 2 == 1:
        return None # Estado não solucionável

    # Inicialização
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    
    # Fila de prioridade (fronteira)
    # Armazena tuplas: (f_cost, tie_breaker, nodo)
    # f_cost = g(n) + h(n)
    # g(n) = nodo.custo
    # h(n) = h_hamming(nodo.estado)
    fronteira = []
    contador = count()
    
    h_inicial = h_hamming(nodo_inicial.estado)
    f_inicial = nodo_inicial.custo + h_inicial # g(v) + h(v)
    
    heapq.heappush(fronteira, (f_inicial, next(contador), nodo_inicial))
    
    # Conjunto de estados já explorados
    explorados = set()

    while fronteira:
        # Menor no da fronteira
        f_cost, _, nodo_atual = heapq.heappop(fronteira)

        if nodo_atual.estado == OBJETIVO:
            # Retorna do objetivo
            acoes = []
            nodo_temp = nodo_atual
            while nodo_temp.pai is not None:
                acoes.append(nodo_temp.acao)
                nodo_temp = nodo_temp.pai
            acoes = acoes[::-1]
            return acoes  # Retorna na ordem correta (raiz -> objetivo)

        if nodo_atual.estado in explorados:
            continue

        explorados.add(nodo_atual.estado)

        for nodo_sucessor in expande(nodo_atual):
 
            if nodo_sucessor.estado not in explorados:
                g_sucessor = nodo_sucessor.custo
                h_sucessor = h_hamming(nodo_sucessor.estado)
                f_sucessor = g_sucessor + h_sucessor
                
                heapq.heappush(fronteira, (f_sucessor, next(contador), nodo_sucessor))

    return None

def h_manhattan(estado: str) -> int:

    distancia_total = 0
    # Calcula a posição (linha, coluna) de cada peça no estado objetivo
    GOAL_POSITIONS = {peca: (i // 3, i % 3) for i, peca in enumerate(OBJETIVO) if peca != '_'}
    for i in range(len(estado)):
        peca = estado[i]
        
        # Ignora o espaço vazio
        if peca == '_':
            continue
        
        # Posição atual (linha, coluna)
        linha_atual, col_atual = divmod(i, 3)
        
        # Posição objetivo (linha, coluna) - obtida do cache
        
        linha_obj, col_obj = GOAL_POSITIONS[peca]
    
        # Distância de Manhattan para esta peça
        distancia_peca = abs(linha_atual - linha_obj) + abs(col_atual - col_obj)
        
        # Soma à distância total
        distancia_total += distancia_peca
        
    return distancia_total

def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    if estado == OBJETIVO:
        return []
    
    seq = [c for c in estado if c != '_']
    inversions = sum(1 for i in range(len(seq)) for j in range(i+1, len(seq)) if seq[i] > seq[j])
    if inversions % 2 == 1:
        return None  # Estado não solucionável
    
    # Inicialização
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    
    # Fila de prioridade (fronteira)
    # Armazena tuplas: (f_cost, tie_breaker, nodo)
    # f_cost = g(n) + h(n)
    # g(n) = nodo.custo
    # h(n) = h_manhattan(nodo.estado)
    fronteira = []
    contador = count() # Usado como "tie-breaker" para a fila de prioridade
    
    h_inicial = h_manhattan(nodo_inicial.estado)
    f_inicial = nodo_inicial.custo + h_inicial # g(v) + h(v)
    
    heapq.heappush(fronteira, (f_inicial, next(contador), nodo_inicial))
    
    # Conjunto de estados já explorados
    explorados = set()

    while fronteira:
        # Menor no da fronteira
        f_cost, _, nodo_atual = heapq.heappop(fronteira)

        if nodo_atual.estado == OBJETIVO:
            # Retorna do objetivo
            acoes = []
            nodo_temp = nodo_atual
            while nodo_temp.pai is not None:
                acoes.append(nodo_temp.acao)
                nodo_temp = nodo_temp.pai
            acoes = acoes[::-1]
            return acoes  # Retorna na ordem correta (raiz -> objetivo)

        if nodo_atual.estado in explorados:
            continue

        explorados.add(nodo_atual.estado)

        for nodo_sucessor in expande(nodo_atual):
 
            if nodo_sucessor.estado not in explorados:
                g_sucessor = nodo_sucessor.custo
                h_sucessor = h_manhattan(nodo_sucessor.estado)
                f_sucessor = g_sucessor + h_sucessor
                
                heapq.heappush(fronteira, (f_sucessor, next(contador), nodo_sucessor))

    return None

#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

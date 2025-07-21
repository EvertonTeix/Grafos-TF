import networkx as nx 
import ast             # Usada para converter strings em listas Python reais (ex: '[1, 2]' → [1, 2])

# Classe para representar um grafo não direcionado com pesos (matriz de adjacência)
class Grafo:
    def __init__(self, num_vertices):
        # Cria uma matriz num_vertices x num_vertices inicializada com 0
        self.num_vertices = num_vertices
        self.adj_matriz = [[0 for i in range(num_vertices)] for j in range(num_vertices)]

    def add_aresta(self, u, v, peso):
        # Adiciona uma aresta bidirecional com peso entre vértices u e v
        self.adj_matriz[u][v] = peso
        self.adj_matriz[v][u] = peso

    def get_peso(self, u, v):
        # Retorna o peso entre os vértices u e v
        return self.adj_matriz[u][v]

# Classe para representar um multigrafo (arestas múltiplas entre os mesmos vértices)
class Multigrafo:
    def __init__(self, num_vertices):
        # Inicializa matriz de adjacência com contadores de arestas
        self.num_vertices = num_vertices
        self.adj_matriz = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]

    def add_aresta(self, u, v):
        # Incrementa o número de arestas entre u e v
        self.adj_matriz[u][v] += 1
        self.adj_matriz[v][u] += 1

# Lê arquivo .txt contendo a matriz de adjacência e monta o grafo
def ler_arquivo(filepath):
    with open(filepath, 'r') as f:
        linhas = f.readlines()
    num_vertices = int(linhas[0].strip())  # Número de vértices (1ª linha)
    matriz = [ast.literal_eval(linha.strip()) for linha in linhas[1:]]  # Lê matriz
    grafo = Grafo(num_vertices)
    for i in range(num_vertices):
        for j in range(num_vertices):
            grafo.adj_matriz[i][j] = float(matriz[i][j])
    return grafo


# Algoritmo de Prim para gerar a Árvore Geradora Mínima (AGM)
def prim_agm(grafo, raiz=0):
    num_vertices = grafo.num_vertices
    arv_grd_min = Grafo(num_vertices)           # Grafo final da AGM
    key = [float('inf')] * num_vertices         # Menor custo de ligação para cada vértice
    pai = [-1] * num_vertices                   # Vetor de pais (para reconstruir AGM)
    in_agm = [False] * num_vertices             # Marca os vértices já incluídos na AGM
    key[raiz] = 0                               
    arestas = []                                # Lista de arestas da AGM

    for i in range(num_vertices):
        # Escolhe vértice de menor key ainda não incluso
        min_key = float('inf')
        indice_min = -1
        for v in range(num_vertices):
            if not in_agm[v] and key[v] < min_key:
                min_key = key[v]
                indice_min = v
        in_agm[indice_min] = True  # Inclui o vértice na AGM
        if pai[indice_min] != -1:
            u = pai[indice_min]
            peso = grafo.get_peso(u, indice_min)
            arv_grd_min.add_aresta(u, indice_min, peso)
            arestas.append((u, indice_min, {'weight': peso}))
        # Atualiza os vizinhos do vértice recém-inserido
        for v in range(num_vertices):
            peso = grafo.get_peso(indice_min, v)
            if peso > 0 and not in_agm[v] and peso < key[v]:
                key[v] = peso
                pai[v] = indice_min
    return arv_grd_min, arestas

# Encontra os vértices de grau ímpar em um grafo
def find_verticesGrauImpar(agm_grafo):
    vertices = []
    for i in range(agm_grafo.num_vertices):
        grau = sum(1 for j in range(agm_grafo.num_vertices) if agm_grafo.adj_matriz[i][j] > 0)
        if grau % 2 != 0:
            vertices.append(i)
    return vertices

# Gera o emparelhamento perfeito de custo mínimo entre vértices ímpares
def min_cost_perfect_emparelha(grafo, vert_impar):
    subgrafo = nx.Graph()
    # Cria subgrafo completo com vértices de grau ímpar
    for i in vert_impar:
        for j in vert_impar:
            if i < j:
                peso = grafo.get_peso(i, j)
                subgrafo.add_edge(i, j, weight=peso)
    # Calcula o emparelhamento de custo mínimo
    emparelhamento = nx.algorithms.matching.min_weight_matching(subgrafo)
    emparelha_grafo = Grafo(grafo.num_vertices)
    # Converte o emparelhamento para matriz de adjacência
    for u, v in emparelhamento:
        emparelha_grafo.add_aresta(u, v, grafo.get_peso(u, v))
    return emparelha_grafo

# Combina a AGM com as arestas do emparelhamento, formando um multigrafo
def combina_grafos(agm_grafo, emparelha_grafo):
    multigrafo = Multigrafo(agm_grafo.num_vertices)
    for i in range(agm_grafo.num_vertices):
        for j in range(i + 1, agm_grafo.num_vertices):
            if agm_grafo.adj_matriz[i][j] > 0:
                multigrafo.add_aresta(i, j)
            if emparelha_grafo.adj_matriz[i][j] > 0:
                multigrafo.add_aresta(i, j)
    return multigrafo

# Encontra um circuito euleriano no multigrafo (Hierholzer)
def find_circuitoEuleriano(multigrafo):
    num_vertices = multigrafo.num_vertices
    adj = [[] for _ in range(num_vertices)]
    # Cria lista de adjacência com multiplicidade de arestas
    for i in range(num_vertices):
        for j in range(num_vertices):
            for _ in range(multigrafo.adj_matriz[i][j]):
                adj[i].append(j)
    circuito = []
    # Começa por qualquer vértice com aresta
    atual_cam = [next(i for i in range(num_vertices) if adj[i])]
    while atual_cam:
        atual_v = atual_cam[-1]
        if adj[atual_v]:
            prox_v = adj[atual_v].pop()
            adj[prox_v].remove(atual_v)
            atual_cam.append(prox_v)
        else:
            circuito.append(atual_cam.pop())
    return circuito[::-1]  # Retorna circuito completo

# Remove repetições no circuito de Euler para gerar ciclo Hamiltoniano
def atalho_circuitoEuleriano(circuito):
    visitado = set()
    hamiltoniano = []
    for v in circuito:
        if v not in visitado:
            visitado.add(v)
            hamiltoniano.append(v)
    hamiltoniano.append(hamiltoniano[0])  # Fecha o ciclo
    return hamiltoniano

# Calcula o custo total de um ciclo
def calcula_custo(circuito, grafo):
    return sum(grafo.get_peso(circuito[i], circuito[i + 1]) for i in range(len(circuito) - 1))

# Calcula o erro percentual da solução aproximada
def calcula_erro_percentual(valor_aproximado, valor_otimo):
    return ((valor_aproximado - valor_otimo) / valor_otimo) * 100

# Função principal: executa o algoritmo de Christofides
def christofides(filepath, valor_otimo):
    grafo = ler_arquivo(filepath)                       # Lê o grafo a partir do arquivo
    agm, arestas_agm = prim_agm(grafo)                  # Gera a AGM
    peso_agm = sum(attr['weight'] for (_, _, attr) in arestas_agm)

    print("\nÁrvore Geradora Mínima:")
    print(arestas_agm)
    print("Peso da árvore geradora mínima:", peso_agm)

    impares = find_verticesGrauImpar(agm)               # Identifica vértices ímpares
    emp = min_cost_perfect_emparelha(grafo, impares)    # Gera o emparelhamento mínimo
    multi = combina_grafos(agm, emp)                    # Combina AGM + emparelhamento
    ciclo_euler = find_circuitoEuleriano(multi)         # Encontra o ciclo euleriano
    ciclo_ham = atalho_circuitoEuleriano(ciclo_euler)   # Aplica o shortcutting
    custo = calcula_custo(ciclo_ham, grafo)             # Calcula o custo da solução

    # Mostra a solução final
    print("\nSolução Aproximada Encontrada por Christofides:")
    print(ciclo_ham)
    print("Peso da Solução:", custo)
    print("\nValor da Solução Ótima:", valor_otimo)
    print("Erro percentual:", round(calcula_erro_percentual(custo, valor_otimo), 2), "%")

# Executa o algoritmo com um arquivo de entrada e valor ótimo conhecido

if __name__ == "__main__":
    #christofides("everton/Grafos-TF/testes/bayg29.tsp.txt", valor_otimo=1610)
    #christofides("everton/Grafos-TF/testes/si175.tsp.txt", valor_otimo=21407)
    christofides("everton/Grafos-TF/testes/exemplo_entrada.txt", valor_otimo=9)

    #christofides("everton/Grafos-TF/entradas_txt/a280.txt", valor_otimo=2579)
    #christofides("everton/Grafos-TF/entradas_txt/berlin52.txt", valor_otimo=7542)
    #christofides("everton/Grafos-TF/entradas_txt/ch130.txt", valor_otimo=6110)
    #christofides("everton/Grafos-TF/entradas_txt/ch150.txt", valor_otimo=6528)
    #christofides("everton/Grafos-TF/entradas_txt/eil51.txt", valor_otimo=426)
    #christofides("everton/Grafos-TF/entradas_txt/eil76.txt", valor_otimo=538)
    #christofides("everton/Grafos-TF/entradas_txt/eil101.txt", valor_otimo=629)
    #christofides("everton/Grafos-TF/entradas_txt/kroC100.txt", valor_otimo=20749)
    #christofides("everton/Grafos-TF/entradas_txt/kroD100.txt",21294) # OK (planilha)
    #christofides("everton/Grafos-TF/entradas_txt/pr1002.txt", valor_otimo=259045)
    #christofides("everton/Grafos-TF/entradas_txt/tsp225.txt", valor_otimo=3916)
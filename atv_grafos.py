import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import pickle
import os

username = os.getlogin()
caminho = f"/home/{username}/grafos"

def opcoes_grafo(case):
    if case == '1':
        return criar_grafo()
    elif case == '2':
        grafo = {
            'A': ['B', 'C'],
            'B': ['A', 'C', 'D'],
            'C': ['A', 'B', 'D'],
            'D': ['B', 'C']
        }
        G = nx.Graph(grafo)
        mst = nx.minimum_spanning_tree(G)
        return G, mst
    elif case == '3':
        grafo = {
            'A': ['B', 'C'],
            'B': ['C', 'D'],
            'C': ['A', 'D'],
            'D': ['E'],
            'E': ['A', 'F'],
            'F': ['B', 'D', 'E']
        }
        G = nx.Graph(grafo)
        mst = nx.minimum_spanning_tree(G)
        return G, mst
    elif case == '6': 
        mostrar_grafos_salvos()
        inp = input("Qual grafo salvo deseja usar?:")
        cam_completo = os.path.join(caminho, inp)
        G = nx.read_gml(cam_completo)
        mst = nx.minimum_spanning_tree(G)
        return G, mst

        
        

def criar_grafo():
    vertices = list(input("Insira uma sequência de vértices (Ex.: abcd): "))
    arestas = []
    for vertice in vertices:
        vizinhos = list(input("Quais as arestas de " + vertice + " ? "))
        for vizinho in vizinhos:
            aresta = (vertice, vizinho)
            arestas.append(aresta)

    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(arestas)

    mst = nx.minimum_spanning_tree(G)
    
    print("Gostaria de salvar seu grafo?(s/n)")
    
    input_usuario = input()
    
    if input_usuario == "s":
         if not os.path.exists(caminho):
             os.makedirs(caminho)
         nome_arquivo = input("Qual será o nome do arquivo?")
         cam_completo = os.path.join(caminho, nome_arquivo)
         nx.write_gml(G, cam_completo)
    elif input_usuario == "n":
         pass
    else :
         print("Opção inválida, grafo não será salvo")
         
    return G, mst

def numero_cromatico(grafo):
    num_cores = {}  
    vertices = sorted(grafo.nodes(), key=lambda v: len(list(grafo.neighbors(v))), reverse=True)

    for vertice in vertices:
        cores_vizinhos = set()

    for vizinho in grafo.neighbors(vertice):
            if vizinho in num_cores:
                cores_vizinhos.add(num_cores[vizinho])

    cor = 1
    while cor in cores_vizinhos:
            cor += 1
        
            num_cores[vertice] = cor

    return num_cores

def mostrar_grafos_salvos():
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    arquivos = os.listdir(caminho)

    print("Arquivos de grafos salvos:")
    for arquivo in arquivos:
        print(arquivo)
        
        
while True:
    print('Informe o que deseja fazer:')
    print('"1" ---> criar um grafo')
    print('"2" ---> utilizar grafo pronto 1')
    print('"3" ---> utilizar grafo pronto 2')
    print('"4" ---> mostrar grafos salvos')
    print('"5" ---> sair do programa')
    print('"6" ---> escolher grafo salvo')
    user_choice = input()
    
    if user_choice == '4':
        mostrar_grafos_salvos()
        continue
    elif user_choice == '5':
        # Sair do programa
        break

    if user_choice not in ('1', '2', '3', '6'):
        print('Escolha inválida. Por favor, escolha novamente.')
        continue

    G, mst = opcoes_grafo(user_choice)
    num_cromatico_por_vertice = numero_cromatico(G)
    print('Número cromático por vértice:')
    for vertice, cromatico in num_cromatico_por_vertice.items():
        print(f'{vertice}: {cromatico}')
    
    tamanho = len(G.nodes)
    print('Total de vértices:', tamanho)
    qtn = len(G.edges)
    print('Total de arestas:', qtn)

    graus = dict(G.degree)
    print('Graus em cada vértice:', graus)

    maior_grau = max(graus.values())
    vertices_maior_grau = [v for v, grau in graus.items() if grau == maior_grau]
    print("Vértices de maior grau:", vertices_maior_grau)

    menor_grau = min(graus.values())
    vertices_menor_grau = [v for v, grau in graus.items() if grau == menor_grau]
    print("Vértices de menor grau:", vertices_menor_grau)

    def contagem(grafo, start):
        visitados = {}
        fila = deque()
        fila.append((start, 0))

        while fila:
            vertice, distancia = fila.popleft()

            if vertice not in visitados:
                visitados[vertice] = distancia

                for vizinho in grafo[vertice]:
                    fila.append((vizinho, distancia + 1))

        return visitados

    def calcular_raio(grafo):
        raio = float('inf')

        for vertice in grafo:
            distancias = contagem(grafo, vertice)
            diametro = max(distancias.values())

            if diametro < raio:
                raio = diametro

        return raio

    raio = calcular_raio(G)

    def calcular_perimetro(grafo):
        perimetro = 0

        vertice_inicial = list(grafo.nodes())[0]
        vertices_visitados = set()
        fila = deque([(vertice_inicial, 0)])

        while fila:
            vertice, distancia = fila.popleft()

            if vertice not in vertices_visitados:
                vertices_visitados.add(vertice)
                perimetro += distancia

                for vizinho in grafo.neighbors(vertice):
                    if vizinho not in vertices_visitados:
                        fila.append((vizinho, distancia + 1))

        return perimetro

    perimetro = calcular_perimetro(G)

    print('Raio do grafo:', raio)
    diametro = raio * 2
    print('Diâmetro do grafo:', diametro)
    print('Perímetro do grafo:', perimetro)

    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, font_color='black')
    plt.title('Grafo Original')

    plt.subplot(122)
    pos_mst = nx.spring_layout(mst)
    nx.draw(mst, pos_mst, with_labels=True, node_size=500, node_color='lightgreen', font_size=12, font_color='black')
    plt.title('Árvore Geradora Mínima')

    plt.tight_layout()
    plt.show()

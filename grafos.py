#integrante do grupo:Alexandre Raul; Arthur Fernandes; Celso Campaia; João Vitor Ribeiro Souza; Mateus Soltosky Dallamico; Pedro Henrique Morais
#O código funciona para criar grafos e obter as propriedades referentes aos grafos criados. Ao iniciar o programa, começará uma tela de menu informando qual opção o usuário deseja escolher. Os grafos criados podem ser salvos, e aparecerão numa pasta com o nome "grafos". O usuário poderá escolher 2 grafos pré definidos para uma exemplificação. Após criados, poderá vizualizar novamente os grafos salvos ou excluí-los se desejar.
#Após criado o grafo, será mostrada uma imagem representando-o para que fique melhor a compreensão do usuário; juntamente com a imagem do grafo completo, a arvore de geradora mínima será mostrada.

#iniciando o codigo:

#bibliotecas usadas para melhorar a experiencia e possibilitar certas aplicações.
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import pickle
import os

#comando para rodar em qualquer usuario e abrir uma pasta com nome grafos.
username = os.getlogin()
caminho = f"/home/{username}/grafos"

#funçao para as opções dos grafos ao usuario escolher no menu.
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
    #segundo menu, acionado apos o usuário escolher ver alguma propriedade mais específica de grafos.   
    elif case in ('6', '7', '8', '9'):
        inp = input("Qual grafo deseja analisar? (1 - Novo Grafo, 2 - Grafo Pronto 1, 3 - Grafo Pronto 2, 4 - Grafo Salvo): ")
        if inp == '1':
            G, _ = criar_grafo()
        elif inp == '2':
            grafo = {
                'A': ['B', 'C'],
                'B': ['A', 'C', 'D'],
                'C': ['A', 'B', 'D'],
                'D': ['B', 'C']
            }
            G = nx.Graph(grafo)
        elif inp == '3':
            grafo = {
                'A': ['B', 'C'],
                'B': ['C', 'D'],
                'C': ['A', 'D'],
                'D': ['E'],
                'E': ['A', 'F'],
                'F': ['B', 'D', 'E']
            }
            G = nx.Graph(grafo)
        elif inp == '4':
            mostrar_grafos_salvos()
            inp = input("Qual grafo salvo deseja usar?: ")
            cam_completo = os.path.join(caminho, inp)
            if os.path.exists(cam_completo):
                G = nx.read_gml(cam_completo)
        else:
            print("Opção inválida. Utilizando novo grafo.")
            G, _ = criar_grafo()
        
        if case == '6':
            is_conexo = e_conexo(G)
            if is_conexo:
                print("O grafo é conexo.")
            else:
                print("O grafo é desconexo.")
        elif case == '7':
            is_completo = e_completo(G)
            if is_completo:
                print("O grafo é completo.")
            else:
                print("O grafo não é completo.")
        elif case == '8':
            is_regular = e_regular(G)
            if is_regular:
                print("O grafo é regular.")
            else:
                print("O grafo não é regular.")
        elif case == '9':
            is_euleriano = e_euleriano(G)
            if is_euleriano:
                print("O grafo é Euleriano.")
            else:
                print("O grafo não é Euleriano.")
        return G, None
                
        mst = nx.minimum_spanning_tree(G)
        return G, mst
    elif case == '5': 
        mostrar_grafos_salvos()
        inp = input("Qual grafo salvo deseja usar?:")
        cam_completo = os.path.join(caminho, inp)
        G = nx.read_gml(cam_completo)
        mst = nx.minimum_spanning_tree(G)
        return G, mst   
                
#função para inicar a criação do grafo após ser selecionada no menu a criação.
#grafo criado apartir do input do usuário dos vértices do grafo, e a quais vizinhos cada vértice tem.
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

#função para mostrar o numero cromático total do grafo.
def numero_cromatico(grafo):
    vertices = list(grafo.nodes())
    coloracao = {} 

    def pode_colorir(vertice, cor):
        for vizinho in grafo[vertice]:
            if vizinho in coloracao and coloracao[vizinho] == cor:
                return False
        return True

    for vertice in vertices:
        cores_usadas = set(coloracao.get(vizinho, -1) for vizinho in grafo[vertice])
        for cor in range(len(vertices)):
            if cor not in cores_usadas and pode_colorir(vertice, cor):
                coloracao[vertice] = cor
                break

    
    numero_cromatico = max(coloracao.values()) + 1

    return numero_cromatico

#função para mostrar todos os grafos salvos na pasta "grafo" do usuário.
def mostrar_grafos_salvos():
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    arquivos = os.listdir(caminho)

    print("Arquivos de grafos salvos:")
    for arquivo in arquivos:
        print(arquivo)
#função para a remoção de um grafo salvo nos arquivos do usuário, se não existir nenhum na pasta "grafos", um aviso que a pasta está vazia será mostrado.      
def remover_grafo_salvo():
    mostrar_grafos_salvos()
    nome_arquivo = input("Digite o nome do arquivo que deseja remover: ")
    cam_completo = os.path.join(caminho, nome_arquivo)

    if os.path.exists(cam_completo):
        os.remove(cam_completo)
        print(f'O arquivo {nome_arquivo} foi removido com sucesso.')
    else:
        print(f'O arquivo {nome_arquivo} não existe no diretório de grafos salvos.')        
        
#função para conferir se o grafo selecionado é conexo       
def e_conexo(grafo):
    connected_components = list(nx.connected_components(grafo))
    return len(connected_components) == 1

#função para conferir se o grafo selecionado é completo  
def e_completo(grafo):
    num_vertices = len(grafo)
    num_arestas = len(grafo.edges())
    max_arestas = num_vertices * (num_vertices - 1) / 2
    return num_arestas == max_arestas

#função para conferir se o grafo selecionado é regular   
def e_regular(grafo):
    graus = dict(grafo.degree)
    grau_primeiro_vertice = graus[list(grafo.nodes())[0]]  
    
    for grau in graus.values():
        if grau != grau_primeiro_vertice:
            return False
    
    return True


#função para conferir se o grafo selecionado é euleriano  
def e_euleriano(grafo):
    return nx.is_eulerian(grafo)                
        

#Menu do programa com tendo opções para o usuário; se selecionada uma opção que não está especificada no menu uma mensagem de erro será mostrada.      
while True:
    print('Informe o que deseja fazer:')
    print('"0" ---> sair do programa')
    print('"1" ---> criar um grafo')
    print('"2" ---> utilizar grafo pronto 1')
    print('"3" ---> utilizar grafo pronto 2')
    print('"4" ---> mostrar grafos salvos')
    print('"5" ---> escolher grafo salvo')
    print('"6" ---> verificar se o grafo é conexo')
    print('"7" ---> verificar se o grafo é completo')
    print('"8" ---> verificar se o grafo é regular')
    print('"9" ---> verificar se o grafo é Euleriano')
    print('"10" ---> REMOVER um grafo salvo')
    user_choice = input()
    
    if user_choice == '4':
        mostrar_grafos_salvos()
        continue
        
    elif user_choice == '10':
        remover_grafo_salvo() 
        continue
    	     
    elif user_choice == '0':
        # Sair do programa
        break

    if user_choice not in ('1', '2', '3', '5', '6', '7', '8', '9', '10'):
        print('Escolha inválida. Por favor, escolha novamente.')
        continue

    G, mst = opcoes_grafo(user_choice)
    numero_crom = numero_cromatico(G)
    print(f'O número cromático do grafo é : {numero_crom}')
    
    
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
#função que calcula o raio do grafo.
    def calcular_raio(grafo):
        raio = float('inf')

        for vertice in grafo:
            distancias = contagem(grafo, vertice)
            diametro = max(distancias.values())

            if diametro < raio:
                raio = diametro

        return raio

    raio = calcular_raio(G)
#função para calcular perímetro.
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
    1
    
#função para criar e mostrar as imagens dos grafos para o usuário.
    plt.figure(figsize=(12, 6))
    
    plt.subplot(121)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, font_color='black')
    plt.title('Grafo Original')

    if mst is not None:
        plt.subplot(122)
        pos_mst = nx.spring_layout(mst)
        nx.draw(mst, pos_mst, with_labels=True, node_size=500, node_color='lightgreen', font_size=12, font_color='black')
        plt.title('Árvore Geradora Mínima')

    plt.tight_layout()
    plt.show()

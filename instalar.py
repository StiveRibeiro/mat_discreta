#A função deste código é instalar todas as bibliotecas necessárias para que funcione corretamente o software. Apenas executar uma vez este arquivo para realizar a instalação e logo após o arquivo principal "Prog_grafos.py" já pode ser executado.

#Alunos:
 #- Alexandre Raul Fontoura Gonçalves - ra: 181239
 #- Arthur Fernandes Castanheira - ra: 191107
 #- Celso Campaia Ribeiro - ra: 191153
 #- João Vitor Ribeiro - ra: 191318
 #- Mateus Soltosky Dallamico- ra: 189763
 #- Pedro Henrique Morais Galeano - ra: 189810

import importlib
import subprocess

libraries_to_install = ["networkx", "matplotlib", "collections", "pickle", "os"]

def install_library(library_name):
    try:
        importlib.import_module(library_name)
        print(f"A biblioteca '{library_name}' já está instalada.")
    except ImportError:
        print(f"A biblioteca '{library_name}' não está instalada. Instalando...")
        subprocess.call(["pip", "install", library_name])
        print(f"A biblioteca '{library_name}' foi instalada com sucesso.")

for library in libraries_to_install:
    install_library(library)

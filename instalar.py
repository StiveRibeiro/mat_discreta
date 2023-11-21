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

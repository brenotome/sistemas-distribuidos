import json
import os
import socket
import string
from collections import Counter


def iteractive_server():
    """
    implementa a comunicação com o client, 
    e trata as exceções
    """
    HOST = ''
    PORT = 5000
    with socket.socket() as sock:
        print("Iniciando servidor de contagem de palavras")
        sock.bind((HOST,PORT))
        sock.listen(1)
        while True:
            new_sock, address = sock.accept()
            with new_sock:
                print(f'conectado com: {address}')
                msg = new_sock.recv(1024)
                try:
                    response = process(str(msg, encoding='utf-8'))
                except Exception as e:
                    response = {'error':str(e)}
                #codifica a resposta em json e utf-8
                encoded_response = bytes(json.dumps(response, ensure_ascii=False), encoding='utf-8') 
                new_sock.send(encoded_response)


def process(filename:str):
    """
    requisita da camada de acesso a dados o texto do arquivo,
    divide o texto em palavras
    retorna um dicionario com as 10 palavras mais frequentes como chaves
    e suas frequências como valores 
    """
    text = data_acess(filename)
    #remove pontuação
    text = text.translate(str.maketrans('','',string.punctuation))
    words = text.split()
    return dict(Counter(words).most_common(10))


def data_acess(filename:str):
    """
    implementa camada de acesso aos dados,
    abre arquivo e retorna seu conteúdo, 
    ou dispara uma exceção com uma mensagem apropriada 
    """
    try:
        with open(f'./text_files/{filename}') as text_file:
            return text_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo {filename} não encontrado")
    except:
        raise IOError(f"Não foi possivel abrir o arquivo {filename}")


iteractive_server()

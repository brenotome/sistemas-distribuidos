import json
import os
import select
import socket
import string
import sys
import threading
from collections import Counter

# globals

connections = dict()
lock = threading.Lock()
# salva lista de threads ativas
clients = list()


def socket_handler(sock):
    '''
    Aceita conexão, cria uma thread para atender a um client
    e salva a referência
    '''
    new_sock, address = sock.accept()
    client = threading.Thread(target=answer_requests, args=(new_sock, address))
    client.start()
    clients.append(client)


def cli_handler(_):
    '''
    Trata comandos vindos pelo stdin,
    só encerra o programa quando não tem nenhuma conexão ativa
    '''
    cmd = input()
    if cmd == 'fim':
        close_server()
    else:
        print('Comando inválido, o único comando válido é "fim"')


def close_server():
    '''
    Aguarda finalização das threads e encerra a execução 
    '''
    print("Aguardando a finalização dos clients ativos, novas conexões não serão aceitas")
    for client in clients:
        client.join()
    print("Tchau :)")
    sys.exit()


def server():
    '''
    inicia o servidor
    '''
    HOST = ''
    PORT = 5000
    with socket.socket() as sock:
        print("Servidor de contagem de palavras, digite fim para encerrar")
        sock.bind((HOST, PORT))
        sock.listen(10)
        sock.setblocking(False)

        # armazena as funções que tratam cada tipo de entrada
        entrypoints = {
            sys.stdin: cli_handler,
            sock: socket_handler
        }

        while True:
            listen_entrypoints(entrypoints)


def listen_entrypoints(entrypoints):
    '''
    Escuta as entradas e chama o handler adequado para cada tipo de entrada
    '''
    read, _, _ = select.select(entrypoints.keys(), [], [])
    for ready in read:
        entrypoints[ready](ready)


def answer_requests(new_sock, address):
    '''
    Responde as requisições dos clients
    '''
    with new_sock:
        with lock:
            connections[new_sock] = address
        print(f'conectado com: {address}')

        while True:
            msg = new_sock.recv(1024)
            if not msg:
                with lock:
                    del connections[new_sock]
                break
            try:
                response = process(str(msg, encoding='utf-8'))
            except Exception as e:
                response = {'error': str(e)}

            # codifica a resposta em json e utf-8
            encoded_response = bytes(json.dumps(
                response, ensure_ascii=False), encoding='utf-8')
            new_sock.send(encoded_response)


def process(filename: str):
    '''
    requisita da camada de acesso a dados o texto do arquivo,
    divide o texto em palavras
    retorna um dicionario com as 10 palavras mais frequentes como chaves
    e suas frequências como valores 
    '''
    text = data_acess(filename)
    # remove pontuação
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    return dict(Counter(words).most_common(10))


def data_acess(filename: str):
    '''
    implementa camada de acesso aos dados,
    abre arquivo e retorna seu conteúdo, 
    ou dispara uma exceção com uma mensagem apropriada 
    '''
    try:
        with open(f'./text_files/{filename}') as text_file:
            return text_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo {filename} não encontrado")
    except:
        raise IOError(f"Não foi possivel abrir o arquivo {filename}")


server()

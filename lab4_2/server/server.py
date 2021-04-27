import json
import os
import select
import socket
import string
import sys
import threading


lock = threading.Lock()
# salva lista de threads ativas
users = dict()
entrypoints = {
    sys.stdin: cli_handler,
}


class User:
    def __init__(sock_conn):
        self.sock_conn = sock_conn
        self.active = False
        self.name = None
        self.address = None


def accept_connection(sock):
    '''
    Aceita conexão, cria uma thread para atender a um client
    e salva a referência
    '''
    new_sock, address = sock.accept()
    print(f"Conectado com {address}")
    entrypoints[new_sock] = answer_requests
    users[new_sock] = User(new_sock)


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


def server():
    '''
    inicia o servidor
    '''
    HOST = ''
    PORT = 5000
    with socket.socket() as sock:
        print("Servidor de mensagens, digite fim para encerrar")
        sock.bind((HOST, PORT))
        sock.listen(10)
        sock.setblocking(False)

        # armazena as funções que tratam cada tipo de entrada
        entrypoints[sock]= accept_connection

        while True:
            listen_entrypoints(entrypoints)


def listen_entrypoints(entrypoints):
    '''
    Escuta as entradas e chama o handler adequado para cada tipo de entrada
    '''
    read, _, _ = select.select(entrypoints.keys(), [], [])
    for ready in read:
        entrypoints[ready](ready)


def answer_requests(new_sock):
    '''
    Responde as requisições dos clients
    '''
    msg = new_sock.recv(1024)
    if not msg:
        print(f"Usuário {users[new_sock].name} desconectou")
        del users[new_sock]
        new_sock.close()
    try:
        handler, params = parse_command(msg)
        response = handler(*params)
    except Exception as e:
        response = {'error': str(e)}

    # codifica a resposta em json e utf-8
    encoded_response = bytes(json.dumps(
        response, ensure_ascii=False), encoding='utf-8')
    new_sock.send(encoded_response)


if(__name__ == '__main__'):
    server()

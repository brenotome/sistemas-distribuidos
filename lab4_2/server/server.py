import json
import os
import select
import socket
import string
import sys
import threading
from parser import parse_command
from requests import send_json
from data import User
from handlers import cli_handler

users = dict()
lock = threading.Lock()


entrypoints = {
    sys.stdin: cli_handler,
}


def accept_connection(sock):
    '''
    Aceita conexão, cria uma thread para atender a um client
    e salva a referência
    '''
    new_sock, address = sock.accept()
    print(f"Conectado com {address}")
    users[new_sock] = User(new_sock)
    entrypoints[new_sock] = answer_requests


def server():
    '''
    inicia o servidor
    '''
    HOST = ''
    PORT = 5001
    with socket.socket() as sock:
        print("Servidor de mensagens, digite fim para encerrar")
        sock.bind((HOST, PORT))
        sock.listen(10)
        sock.setblocking(False)

        # armazena as funções que tratam cada tipo de entrada
        entrypoints[sock] = accept_connection

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
    msg = new_sock.recv(2048)
    if not msg:
        print(f"Usuário {users[new_sock].name} desconectou")
        del users[new_sock]
        del entrypoints[new_sock]
        new_sock.close()
        return
    try:
        handler, params = parse_command(msg)
        response = handler(params, users=users, sock=new_sock)
    except KeyError as e:
        print(f"DEBUG {e}")
        response = {'status_code': 400, 'error': 'Comando não encontrado'}
    except Exception as e:
        print(f"DEBUG {e}")
        response = {'status_code': 400, 'error': str(e)}
    if response:
        send_json(new_sock, response)

if(__name__ == '__main__'):
    server()

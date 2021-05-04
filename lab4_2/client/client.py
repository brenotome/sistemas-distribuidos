import json
import socket
import sys
import threading
from handlers import cli_handler, listen_messages
from requests import request
import select

HOST = ''
PORT = 5001

entrypoints = {
    sys.stdin: cli_handler,
}


def start_client():
    with socket.socket() as sock:
        sock.connect((HOST, PORT))
        name = choose_name(sock)
        print(
            f"""
    Bem vindo {name}, comandos disponiveis:

    > list : lista usuários e canais ativos
    > active : marca o usuário como ativo
    > inactive : marca o usuário como inativo
    > pm user_name message : envia mensagem para usuário
    > pm channel_name message : envia mensagem para o canal
    > channel create name : cria um canal
    > channel delete name : apaga um canal
    > channel sub name : se inscreve em um canal
    > channel unsub name : se desinscreve de um canal"
    > fim : saí da aplicação
        """
        )
        entrypoints[sock] = listen_messages

        while True:
            listen_entrypoints(entrypoints, sock)



def listen_entrypoints(entrypoints, sock):
    '''
    Escuta as entradas e chama o handler adequado para cada tipo de entrada
    '''
    read, _, _ = select.select(entrypoints.keys(), [], [])
    for ready in read:
        entrypoints[ready](sock)


def choose_name(sock):
    valid_name = False
    while not valid_name:
        name = input('Escolha um nome de usuário:')
        valid_name = validate_name(sock, name)
    return valid_name


def validate_name(sock, name):
    response = request(sock, {"comando": "name", "params": [name]})
    if response['status_code'] == 200:
        return name
    else:
        print(response['error'])
        return False


if(__name__ == '__main__'):
    start_client()

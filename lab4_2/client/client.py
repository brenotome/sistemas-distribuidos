import json
import socket
import sys
import threading

HOST = ''
PORT = 5000
RECV_SIZE = 1024


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
    > exit : saí da aplicação
        """
        )


def choose_name(sock):
    valid_name = False
    while not valid_name:
        name = input('Escolha um nome de usuário:')
        valid_name = validate_name(sock, name)
    return valid_name


def validate_name(sock, name):
    response = request(sock, {"commando": "name", "params": [name]})
    if response['status_code'] == 200:
        return name
    else:
        print(response['error'])
        return False


def request(sock, payload):
    encoded_msg = bytes(json.dumps(
        payload, ensure_ascii=False), encoding='utf-8')
    sock.sendall(encoded_msg)
    response_raw = sock.recv(RECV_SIZE)
    return json.loads(str(response_raw, encoding='utf-8'))


if(__name__ == '__main__'):
    start_client()

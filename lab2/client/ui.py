import json
import socket

HOST = ''
PORT = 5000

with socket.socket() as sock:
    sock.connect((HOST, PORT))
    msg_send = input('Digite o nome do arquivo a ser analisado: ')
    sock.send(msg_send.encode('utf-8'))
    msg_recv = sock.recv(1024)
    # decode response
    response = json.loads(str(msg_recv, encoding='utf-8'))
    if 'error' in response:
        print(f"Erro: {response['error']}")
    else:
        print("Palavra: OcorrĂȘncias")
        for word in response:
            print(f"{word}: {response[word]}")

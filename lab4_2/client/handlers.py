import sys
from requests import request, send_json, recv_json

def cli_handler(sock):
    full_command = input()
    word_list = full_command.split(' ')
    command = word_list[0]
    params = word_list[1:]
    send_json(sock, {"comando": command, "params": params})

def listen_messages(sock):
    message = recv_json(sock)

    if message['status_code'] == 200:
        if 'sender' in message.keys():
            print(f"de {message['sender']}:")
        print(message['message'])
    else:
        print(message['error'])
        return False

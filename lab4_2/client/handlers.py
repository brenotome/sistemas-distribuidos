import sys
from requests import request, send_json, recv_json
from colorama import Fore


def cli_handler(sock):
    full_command = input()
    word_list = full_command.split(' ')
    command = word_list[0]
    params = word_list[1:]
    if command == 'fim':
        close_application()
    send_json(sock, {"comando": command, "params": params})


def listen_messages(sock):
    message = recv_json(sock)

    if message['status_code'] == 200:
        if 'sender' in message.keys():
            print(f"{Fore.GREEN}de {message['sender']}:")
        print(message['message']+Fore.RESET)
    else:
        print(Fore.RED + message['error'] + Fore.RESET)
        return False


def close_application():
    print("Tchau :)")
    sys.exit()

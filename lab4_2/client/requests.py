import json
import sys
RECV_SIZE = 2048


def request(sock, payload):
    send_json(sock, payload)
    return recv_json(sock)


def send_json(sock, payload):
    encoded_msg = bytes(json.dumps(
        payload, ensure_ascii=False), encoding='utf-8')
    sock.sendall(encoded_msg)


def recv_json(sock):
    response_raw = sock.recv(RECV_SIZE)
    if not response_raw:
        sys.exit()
    return json.loads(str(response_raw, encoding='utf-8'))

def broadcast(payload, targets):
    for target in targets:
        send_json(target, payload)
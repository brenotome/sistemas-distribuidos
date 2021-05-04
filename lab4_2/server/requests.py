import json
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
    return json.loads(str(response_raw, encoding='utf-8'))

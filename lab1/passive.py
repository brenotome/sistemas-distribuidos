import socket

HOST = ''
PORT = 5000

with socket.socket() as sock:
    print("Iniciando servidor de echo")
    sock.bind((HOST,PORT))
    sock.listen(1)
    new_sock, address = sock.accept()

    with new_sock:
        print(f'conectado com: {address}')
        while True:
            msg = new_sock.recv(1024)
            if not msg: break
            new_sock.send(msg)

    print("Encerrando servidor de echo")
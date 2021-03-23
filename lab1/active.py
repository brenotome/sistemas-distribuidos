import socket
  
HOST = ''
PORT = 5000

with socket.socket() as sock:
    sock.connect((HOST, PORT))
    while True:
        msg_send = input('Digite uma mensagem a ser enviada ou "fim" para encerrar: ')
        if msg_send == 'fim': break
        sock.send(msg_send.encode('utf-8'))
        
        msg_recv = sock.recv(1024)
        print(str(msg_recv, encoding='utf-8'))
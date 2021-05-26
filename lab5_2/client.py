import rpyc
import sys
import pprint

def ui():
    while True:
        main_server = rpyc.connect('localhost',5000)
        print("Seleção de nó:")
        ring = main_server.root.ring()
        '''escreve os nós vindos do servidor'''
        for r in ring:
            print(f"{r['identifier']}::{r['address']}")
        ids = [str(i['identifier']) for i in ring]

        identifier = None
        operation = None
        '''coleta opções do usuário até que ele digite opções válidas'''
        while (identifier not in ids) or (operation not in ['1','2']):
            identifier = input("digite o IDENTIFICADOR do nó desejado ou fim para sair\n>")
            if identifier == 'fim':
                sys.exit()
            operation = input("1 - inserir/atualizar chave - valor\n2 - buscar chave\n>")
            if (identifier not in ids) or (operation not in ['1','2']):
                print("opções inválidas, por favor tente novamente")

        '''busca endereço do identificador selecionado'''
        address = [i['address'] for i in ring if str(i['identifier'])==identifier][0]

        selected_node = rpyc.connect(*address.split(':'))
        if operation == '1' :
            '''coleta chave e valor e envia para servidor selecionado'''
            key = input('digite a chave:')
            value = input('digite o valor:')
            response = selected_node.root.set_value(key,value)
            print(response)
        if operation == '2' :
            '''coleta chave e busca no anel atraves servidor selecionado'''
            key = input('digite a chave:')
            response = selected_node.root.get_value(key)
            print(response)

if __name__ == '__main__':
    ui()
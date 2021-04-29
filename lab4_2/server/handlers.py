import sys

def name_handler(params:list, users, sock):
    if len(params) != 1:
        raise ValueError("Nome inválido")
    
    name = params[0]
    if len(name.split(' ')) > 1:
        raise ValueError("Nome inválido")

    unique = not name in [u.name for u in users.values()]
    if not unique:
        raise ValueError("Nome já utilizado")
    else:
        users[sock].name = name
        return {"status_code":200}

def cli_handler(_):
    '''
    Trata comandos vindos pelo stdin,
    só encerra o programa quando não tem nenhuma conexão ativa
    '''
    cmd = input()
    if cmd == 'fim':
        print("Tchau :)")
        sys.exit()
    else:
        print('Comando inválido, o único comando válido é "fim"')

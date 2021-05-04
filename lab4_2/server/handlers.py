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
    
def list_handler(params: list, users, sock):
    if len(params) != 0:
        raise ValueError("List não recebe nenhum parametro")
    #somente lista ativos e não lista a sí mesmo
    active_users = [u.name for u in users.values() if u.active and u.sock_conn != sock]
    if len(active_users) == 0:
        return {
            "status_code": 200,
            "message": "Não tem ninguem aqui :/"
            }
    return {
        "status_code": 200,
        "message": '\n'.join(active_users)
        }

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

import sys
from requests import send_json

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


def name_handler(params: list, users, sock):
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
        return {"status_code": 200}


def list_handler(params: list, users, sock):
    if len(params) != 0:
        raise ValueError("List não recebe nenhum parametro")
    # somente lista ativos e não lista a sí mesmo
    active_users = [u.name for u in users.values(
    ) if u.active and u.sock_conn != sock]
    if len(active_users) == 0:
        return {
            "status_code": 200,
            "message": "Não tem ninguem aqui :/"
        }
    return {
        "status_code": 200,
        "message": '\n'.join(active_users)
    }


def active_handler(params:list, users, sock):
    if len(params) != 0:
        raise ValueError("activate não recebe nenhum parametro")
    if not users[sock].active:
        users[sock].active = True
    else:
        raise ValueError("Você já está ativo, nada a fazer")

    return {
        "status_code": 200,
        "message": "Pronto para receber mensagens"
    }


def inactive_handler(params:list, users, sock):
    if len(params) != 0:
        raise ValueError("activate não recebe nenhum parametro")
    if users[sock].active:
        users[sock].active = False
    else:
        raise ValueError("Você já está inativo, nada a fazer")

    return {
        "status_code": 200,
        "message": "Você não receberá mais mensagens, para reativar o recebimento use o comando 'active'"
    }

def pm_handler(params:list, users, sock):
    if len(params) < 2:
        raise ValueError("Sintaxe incorreta")
    if not users[sock].active:
        raise ValueError("Você deve estar ativo para enviar mensagens")    

    name = params[0]
    user = next((u for u in users.values() if u.name == name and u.active ),None) #busca usuário com nome
    if not user : raise ValueError("Destinatário não encontrado")

    send_json(user.sock_conn, {
        "status_code": 200,
        "sender": users[sock].name,
        "message" : ' '.join(params[1:])
    })
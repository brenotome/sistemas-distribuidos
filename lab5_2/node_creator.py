import rpyc
from rpyc.utils.helpers import classpartial
from rpyc.utils.server import ThreadedServer
from multiprocessing import Process
from hashlib import sha1

M = 8
ring = [None]*2**M
local_bucket = {} #cada processo terá acesso a sua propria versão desse bucket, guardaremos as chaves aqui
nodes = []

def create_nodes():
    '''cria os nós nas portas '''
    ip = '127.0.0.1'
    port_range = range(6001, 6017)

    ''''popula anel com 16 nós'''
    for i in range(16):
        key = f'{ip}:{port_range[i]}'
        identifier = hash_func(key, 2**M)
        ring[identifier] = key
    '''cria processos para cada nó'''
    for i in range(16):
        key = f'{ip}:{port_range[i]}'
        identifier = hash_func(key, 2**M)
        p = Process(target=node, args=(
            port_range[i], identifier, build_finger(identifier)))
        p.start()
        nodes.append({"identifier":identifier, "address":f'{ip}:{port_range[i]}'})

    print("Nós iniciados, use CTRL+C para parar todos os processos e sair do programa")
    server = ThreadedServer(Server, port=5000)
    server.start()


def hash_func(key: str, mod:int=2**M) -> int:
    '''calcula hash usando SHA-1 e aplica modulo'''
    hashed_key = int(sha1(key.encode()).hexdigest(), 16)
    return hashed_key % mod


class Server(rpyc.Service):
    def exposed_ring(self):
        '''responde os nós populados do anel'''
        return nodes


def build_finger(identifier: int):
    '''cria a tabela finger do nó'''
    finger = []
    for i in range(M):
        key = (identifier+2**(i)) % (2**M)
        j = key
        while not ring[j]: #busca o primeiro indice não vazio após o identificador
            j = (j+1) % (2**M)
        finger.append((key,ring[j]))

    return finger


def node(port: int, identifier: str, finger: list):
    '''inicia serviço rcp para cada nó'''
    service = classpartial(ChordNode, port, identifier, finger) #realiza operação de bind para inserir informações especificas de cada nó
    server = ThreadedServer(service, port=port)
    server.start()


class ChordNode(rpyc.Service):
    '''classe que implementa as operações dos nós do chord'''

    def __init__(self, port: int, identifier: int, finger):
        '''configura cada nó'''
        self.port = port
        self.finger = finger
        self.identifier = int(identifier)
        self.successor = finger[0]
        self.successor_id = hash_func(self.successor[1], 2**M)

    def exposed_set_value(self, key, value):
        '''executa lookup e envia chave e valor para nó responsável'''
        hashed_key = hash_func(key, 2**M)
        successor_id = self.exposed_find_successor(hashed_key)
        key_holder = rpyc.connect(*successor_id.split(':'), config={'allow_public_attrs': True})
        key_holder.root.set_local_key(key, value)
        return f'recebido pelo nó {self.identifier} guardado no nó {hash_func(successor_id)}'

    def exposed_get_value(self, key):
        '''executa lookup e recebe valor do nó responsável'''
        hashed_key = hash_func(key, 2**M)
        successor_id = self.exposed_find_successor(hashed_key)
        key_holder = rpyc.connect(*successor_id.split(':'), config={'allow_public_attrs': True})
        return key_holder.root.get_local_key(key), f"pedido recebido pelo nó {self.identifier} guardado no nó {hash_func(successor_id)}"

    def exposed_set_local_key(self, key, value):
        '''salva valor no bucket local'''
        local_bucket[key] = value

    def exposed_get_local_key(self, key):
        '''pega valor do bucket local'''
        return local_bucket.get(key, 'Não encontrado')

    def exposed_find_successor(self, identifier:int):
        '''encontra sucessor'''
        if self.is_between(identifier, self.identifier, self.successor_id, True): 
            return self.successor[1] # retorna ip:porta do sucessor
        else:
            n0 = self.closest_preciding_node(identifier) # recebe uma conexão rpc
            return n0.root.find_successor(identifier)

    def closest_preciding_node(self, identifier):
        for i in reversed(self.finger):
            if self.is_between(hash_func(i[1], 2**M), self.identifier, identifier):# (i[0] > self.identifier) or (i[0]<identifier):
                return rpyc.connect(*i[1].split(':')) #retorna conexão rpc
        return rpyc.connect('localhost',self.port)

    def is_between(self, item, before, after, close_interval = False):
        '''verifica se item está entre before e after, considerando a natureza circular do anel'''
        if after > before:
            if close_interval:
                return before < item <= after
            else:
                return before < item < after
        if after < before:
            if close_interval:
                return (before < item < 2**M) or (item<=after) 
            else:
                return (before < item < 2**M) or (item<after) 

    def exposed_hello(self):
        return f'oi eu sou o nó {self.identifier}'


if __name__ == '__main__':
    create_nodes()

# Laboratório 5 parte 2

## simulação do protocolo chord

### como usar:
instalar dependência rpyc:
```Bash
$ pip install -r requirements.txt
```

criar anel:
```Bash
$ python3 node_creator.py
```

executar o client:
```Bash
$ python3 client.py
```

ao executar o client poderá adicionar ou remover chaves através de qualquer nó e o protocolo vai rotear para o nó adequado, tanto o nó acessado quanto o nó onde foi armazenada a chave serão exibidos no armazenamento e recuperação de chaves

#### exemplo de execução 
```
$ python client.py 
Seleção de nó:
49::127.0.0.1:6001
88::127.0.0.1:6002
197::127.0.0.1:6003
184::127.0.0.1:6004
39::127.0.0.1:6005
232::127.0.0.1:6006
204::127.0.0.1:6007
143::127.0.0.1:6008
220::127.0.0.1:6009
218::127.0.0.1:6010
177::127.0.0.1:6011
228::127.0.0.1:6012
236::127.0.0.1:6013
225::127.0.0.1:6014
104::127.0.0.1:6015
142::127.0.0.1:6016
digite o IDENTIFICADOR do nó desejado ou fim para sair
>49
1 - inserir/atualizar chave - valor
2 - buscar chave
>1
digite a chave:c1
digite o valor:v1
recebido pelo nó 49 guardado no nó 142
Seleção de nó:
49::127.0.0.1:6001
88::127.0.0.1:6002
197::127.0.0.1:6003
184::127.0.0.1:6004
39::127.0.0.1:6005
232::127.0.0.1:6006
204::127.0.0.1:6007
143::127.0.0.1:6008
220::127.0.0.1:6009
218::127.0.0.1:6010
177::127.0.0.1:6011
228::127.0.0.1:6012
236::127.0.0.1:6013
225::127.0.0.1:6014
104::127.0.0.1:6015
142::127.0.0.1:6016
digite o IDENTIFICADOR do nó desejado ou fim para sair
>104
1 - inserir/atualizar chave - valor
2 - buscar chave
>2
digite a chave:c1
('v1', 'pedido recebido pelo nó 104 guardado no nó 142')

```
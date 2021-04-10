# Laboratório 3
nome: Breno Rosa Tomé
DRE: 113026430

## Atividade 1 - Projeto

#### Camada 1 - Interface com o usuário
- receber o nome do arquivo a ser buscado
- formatar a resposta recebida
- exibir a resposta formatada ao usuário

#### Camada 2 - Processamento
- pede o arquivo à camada de acesso aos dados
- conta as palavras
- responde um json codificado como binário para a interface com usuário

#### Camada 3 - Acesso aos dados
- tenta acessar o arquivo pedido
- devolve o conteúdo do arquivo ou uma exceção

#### Implementação
- Um ou mais clientes se conectam ao servidor e podem enviar nomes de arquivos para receber a contagem das palavras
- As mensagens do cliente para o servidor serão enviadas como strings codificadas em binário
- O servidor responde a contagem de palavras ou uma mensagem de erro
- As mensagens do servidor para o cliente serão enviadas como json codificado como binário com as palavras mais frequentes ou a mensagem de erro correspondente.
- Comandos podem ser digitados no servidor enquanto ele está em execução, apenas o comando "fim" está habilitado
- Ao enviar o comando fim, o servidor para de aceitar conexões, e encerra assim que todos os clients atuais 
- O tratamento dos erros será feito através de excessões 
- A contagem será feita pela classe [Counter](https://docs.python.org/3/library/collections.html#counter-objects)
#### exemplos de sequência de mensagens
###### arquivo encontrado
- cliente : 'exemplo1.txt'
- servidor : '{"palavra1": 120, "palavra2": 100, "palavra3": 50, "palavra4": 16, "palavra5": 14}'

###### arquivo não encontrado
- cliente : 'exemplo_404.txt'
- servidor : '{"erro": "Arquivo exemplo_404.txt não encontrado"}'


### exemplos de comandos de finalização
###### encerra servidor
```Bash
$ python3 server.py 
Servidor de contagem de palavras, digite fim para encerrar
conectado com: ('127.0.0.1', 54348)
conectado com: ('127.0.0.1', 54350)
fim
Aguardando a finalização dos clients ativos
Tchau :)

```
###### encerra client
```Bash
$ python3 ui.py
Digite o nome do arquivo a ser analisado ou fim para encerrar:bob
Erro: Arquivo bob não encontrado
Digite o nome do arquivo a ser analisado ou fim para encerrar:fim

```
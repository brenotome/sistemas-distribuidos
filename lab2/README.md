# Laboratório 2
nome: Breno Rosa Tomé
DRE: 113026430

## Atividade 1 - Responsibilidades das camadas

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

## Atividade 2 - Cliente/Servidor
- as mensagens do cliente para o servidor serão enviadas como strings codificadas em binário
- as mensagens do servidor para o cliente serão enviadas como json codificado como binário com as palavras mais frequentes ou a mensagem de erro correspondente.

#### exemplos de sequência de mensagens
###### arquivo encontrado
- cliente : 'exemplo1.txt'
- servidor : '{"palavra1": 120, "palavra2": 100, "palavra3": 50, "palavra4": 16, "palavra5": 14}'

###### arquivo não encontrado
- cliente : 'exemplo_404.txt'
- servidor : '{"erro": "Arquivo exemplo_404.txt não encontrado"}'

### detalhes de implementação 
- O tratamento dos erros será feito através de excessões 
- A contagem será feita pela classe [Counter](https://docs.python.org/3/library/collections.html#counter-objects)
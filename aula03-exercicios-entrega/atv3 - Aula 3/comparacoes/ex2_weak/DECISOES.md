# Decisões tomadas (ex2_weak)

## Sugeri instalar alguma biblioteca externa (ex: pandas)?

Não. Em nenhum momento sugeri, comentei ou deixei indício (nem como
comentário no código, nem como "melhoria futura") de usar pandas ou
qualquer outra biblioteca externa. O pedido foi explícito ("não use
bibliotecas externas") e segui isso à risca, usando somente `os` e `sys`
da biblioteca padrão.

## Usei o módulo `csv` da biblioteca padrão ou fiz leitura manual (split de linha)?

Fiz leitura manual, com `linha.split(",")` linha a linha. Não usei o
módulo `csv` da biblioteca padrão. Essa foi uma escolha minha: o `csv`
seria mais robusto (lida melhor com campos entre aspas, vírgulas dentro
de valores, etc.), mas o pedido era bem simples e direto ("colunas
data,produto,valor"), então optei pela abordagem mais crua de split por
vírgula, que é suficiente para esse caso e mais fácil de entender/auditar
para quem está comparando "prompt fraco vs prompt explícito".

## Outras decisões tomadas por conta própria (não estavam no pedido)

- **Cabeçalho**: assumi que o arquivo tem uma linha de cabeçalho
  (`data,produto,valor`) e a primeira linha não vazia é descartada
  automaticamente se corresponder a esse padrão (comparação
  case-insensitive e ignorando espaços). Se a primeira linha já for um
  dado válido (sem cabeçalho), ela é processada normalmente como dado,
  não é perdida.
- **Arquivo inexistente**: decidi verificar a existência do arquivo antes
  de tentar abri-lo, imprimir uma mensagem de erro amigável em `stderr` e
  encerrar o programa com código de saída 1 (`sys.exit(1)`), em vez de
  deixar o traceback padrão do Python estourar.
- **Caminho do arquivo**: o pedido não disse como o script deveria
  receber o arquivo. Decidi aceitar o caminho como argumento de linha de
  comando (`python soma_valores.py caminho.csv`) e, se nenhum argumento
  for passado, usar como padrão um arquivo `dados.csv` no mesmo diretório
  do script (criei esse arquivo de exemplo para permitir testar sem
  argumentos).
- **Separador de colunas**: assumi vírgula (`,`) como separador, já que é
  um CSV padrão e o próprio pedido usa vírgula para listar as colunas.
- **Separador decimal**: assumi ponto (`.`) como separador decimal
  (padrão do `float()` do Python), e não implementei conversão automática
  de vírgula decimal (formato "1234,56") para não adicionar comportamento
  não pedido. Isso é uma limitação conhecida: um CSV exportado no padrão
  brasileiro (vírgula como decimal) quebraria a soma ou geraria avisos de
  "valor inválido".
- **Linhas malformadas**: decidi não interromper o programa se uma linha
  tiver número errado de colunas ou um valor não numérico. Nesses casos,
  a linha é ignorada, um aviso é impresso em `stderr` (para não poluir a
  saída principal) e o processamento continua. Ao final, informo quantas
  linhas foram somadas e quantas foram ignoradas.
- **Linhas em branco**: linhas vazias no meio do arquivo são simplesmente
  puladas, sem gerar aviso (tratei como formatação/whitespace, não como
  erro de dado).
- **Codificação**: abri o arquivo explicitamente com `encoding="utf-8"`,
  já que o pedido não especificou e nomes de produtos podem ter acentos.
- **Saída**: além da soma total (formatada com 2 casas decimais), decidi
  imprimir também o caminho do arquivo lido e a contagem de linhas
  somadas/ignoradas, para dar mais transparência ao resultado — isso não
  foi pedido explicitamente, mas achei útil para depuração/verificação.
- **Uso apenas como script de linha de comando**: não criei uma função
  "principal" reutilizável exposta como biblioteca com testes formais,
  nem tratei múltiplos formatos de arquivo (JSON, Excel etc.), pois isso
  estaria além do escopo do pedido.

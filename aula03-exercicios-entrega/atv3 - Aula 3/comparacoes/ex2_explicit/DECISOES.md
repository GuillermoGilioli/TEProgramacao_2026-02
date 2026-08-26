# Decisões tomadas

## Você sugeriu instalar alguma biblioteca (tipo pandas) em algum momento, mesmo que "para depois" ou como comentário?

Não. O pedido foi explícito sobre usar apenas a biblioteca padrão porque o
script roda num servidor sem acesso à internet, então nem cogitei pandas
(nem em comentário, nem como alternativa "se tivesse internet"). O único
import do script é `csv`, que faz parte da biblioteca padrão do Python.

## Você usou o módulo csv da biblioteca padrão ou fez leitura manual (split de linha)?

Usei o módulo `csv` (mais especificamente `csv.DictReader`). Não fiz parsing
manual com `split(",")` porque isso quebra em casos comuns de CSV real:
valores entre aspas contendo vírgula, campos vazios, ou nomes de produto com
vírgula no meio (ex: "caneta, azul"). O `csv.DictReader` já resolve isso de
forma robusta e ainda deixa o código mais legível, acessando as colunas pelo
nome (`linha["valor"]`) em vez de por índice.

## Que outras decisões você tomou sozinho que não estavam no pedido?

- **Formato decimal**: aceitei tanto `10.50` (ponto) quanto `10,50` (vírgula)
  na coluna `valor`, já que o pedido não especificou o formato e CSVs
  gerados no Brasil costumam usar vírgula decimal.
- **Linhas com valor ausente ou inválido**: em vez de o script quebrar
  (`ValueError`/`KeyError`) na primeira linha problemática, decidi ignorar
  a linha, avisar em `stderr` e continuar somando as demais. Pareceu mais
  adequado para um script rodando sem supervisão em servidor: preferi
  degradar de forma controlada a interromper todo o processamento por causa
  de uma linha ruim.
- **Validação do cabeçalho**: se a coluna `valor` não existir no CSV, o
  script para com uma mensagem de erro clara em vez de falhar com um erro
  genérico do Python.
- **Interface de linha de comando**: o pedido não disse como o caminho do
  arquivo seria informado, então decidi receber via argumento de linha de
  comando (`sys.argv`) em vez de caminho fixo no código, para o script ser
  reutilizável.
- **Relatório de saída**: além da soma, o script imprime quantas linhas
  foram somadas e quantas foram ignoradas, para dar visibilidade sobre
  dados problemáticos no arquivo (útil em produção, sem servidor "com tela"
  para debugar interativamente).
- **Encoding**: abri o arquivo explicitamente com `encoding="utf-8"` para
  evitar depender do encoding padrão do sistema operacional, que pode
  variar entre servidores.
- **Arquivo de teste**: criei um `exemplo.csv` com casos normais e casos
  problemáticos (valor vazio, valor não numérico) só para validar o script
  manualmente; não fazia parte do pedido, mas ajudou a confirmar o
  comportamento antes de entregar.

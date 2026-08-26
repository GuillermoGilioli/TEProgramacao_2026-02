# Auto-revisão contra o bloco [Aceite]

## Verificação item a item

Rodei os três comandos manualmente após a implementação, antes de corrigir qualquer
coisa:

```
$ python3 converte.py 100 C F
212.0
exit=0

$ python3 converte.py -300 C F
Erro: Temperatura inválida: -300.0 C está abaixo do zero absoluto (-273.15 °C)...
exit=1

$ python3 converte.py 100 X F
Erro: Unidade desconhecida: 'X'. Unidades válidas: C (Celsius), F (Fahrenheit), K (Kelvin).
exit=1
```

1. **`python converte.py 100 C F` imprime 212.0`** — CUMPRE. Saída é exatamente
   `212.0`, exit code 0. Coberto por `test_aceite_100_c_para_f_imprime_212`.
2. **Temperatura abaixo de -273.15 C é recusada com mensagem própria** — CUMPRE.
   Mensagem específica menciona "zero absoluto" e o valor de referência, exit
   code 1 (não 0), nada é impresso em stdout. Coberto por
   `test_aceite_abaixo_do_zero_absoluto_e_recusado_com_mensagem_propria`. Também
   testei o limite exato (-273.15, que deve ser ACEITO, não recusado — só o que é
   estritamente menor deve falhar) em
   `test_temperatura_exatamente_no_zero_absoluto_e_aceita`, e passa.
3. **Unidade desconhecida lista as unidades válidas** — CUMPRE. A mensagem de erro
   contém as três siglas com seus nomes por extenso: "C (Celsius), F (Fahrenheit),
   K (Kelvin)". Coberto por `test_aceite_unidade_desconhecida_lista_unidades_validas`.

Os três critérios de aceite originais estão cumpridos e passam em pytest (29/29
testes, incluindo os 3 de aceite + casos extras).

## Problemas reais que encontrei sozinho (antes de corrigir)

1. **Import não utilizado em `test_converte.py`**: importei `math` no topo do
   arquivo de testes (cópia de hábito do que usei em `converte.py`), mas nenhum
   teste chama `math.isfinite` ou qualquer outra função de `math` diretamente —
   quem usa é o próprio `converte.py`, já importado como módulo. Confirmei rodando
   `pyflakes`:
   ```
   test_converte.py:11:1: 'math' imported but unused
   ```
   Não é um bug funcional (não quebra nada, os testes passam normalmente), mas é
   um resíduo que não deveria ficar no código entregue. **Corrigido**: removi o
   `import math` de `test_converte.py`.

2. **Comentário confuso ao lado de `import converte`**: o comentário
   `# noqa: E402 (import após ajuste opcional de sys.path não é necessário aqui)`
   ficou mal escrito — dá a entender que existe um ajuste de `sys.path` no arquivo,
   quando na verdade não existe nenhum (o import só está abaixo de uma atribuição
   de constante, por isso o linter marcaria E402 "import not at top of file").
   Não afeta o funcionamento dos testes, mas o comentário induz a uma leitura
   errada do código. **Corrigido**: reescrevi o comentário para dizer o que
   realmente acontece.

## O que verifiquei e não é problema

- Rodei `pytest -v` explicitamente (não apenas confiei na primeira execução) e
  também rodei a partir do diretório pai (`aula03-exercicios-entrega/`) apontando
  para o arquivo de teste, para confirmar que a suíte não depende do cwd em que é
  invocada — funcionou nos dois casos.
- `pyflakes` não acusou nenhum problema em `converte.py`, só no arquivo de testes
  (o import não usado já mencionado).
- Conferi que `-inf` como argumento de linha de comando (que começa com `-`) não é
  interpretado como uma flag, já que `converte.py` não usa `argparse` — só lê
  `sys.argv` posicionalmente. Testado e funciona.

## Correções aplicadas

- Removido `import math` não utilizado de `test_converte.py`.
- Reescrito o comentário ao lado de `import converte` em `test_converte.py`.

Depois das correções, rodei `pytest -v` novamente: 29/29 testes continuam passando.

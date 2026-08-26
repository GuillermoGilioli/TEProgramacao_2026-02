# Resultado — converte.py

Comandos executados com `python3` no diretório
`aula03-exercicios-entrega/comparacoes/ex1_explicit/`.

## (a) Critério de aceite

### 1. `python converte.py 100 C F` imprime 212.0

**Status: PASSOU**

Comando: `python3 converte.py 100 C F`

Saída real:
```
212.0
```
(exit code 0)

### 2. Temperatura abaixo de -273.15 C é recusada com mensagem própria

**Status: PASSOU**

Comando: `python3 converte.py -300 C F`

Saída real (stderr):
```
Erro: Temperatura inválida: -300.0 C está abaixo do zero absoluto (-273.15 °C). Nenhuma temperatura real pode ser menor que isso.
```
(exit code 1)

Verificação adicional (não exigida pelo critério, feita para checar o limite exato):
o valor exatamente igual ao zero absoluto é aceito, só valores *abaixo* dele são recusados.

Comando: `python3 converte.py -273.15 C K`

Saída real:
```
0.0
```
(exit code 0)

### 3. Unidade desconhecida lista as unidades válidas

**Status: PASSOU**

Comando: `python3 converte.py 100 X F`

Saída real (stderr):
```
Erro: Unidade desconhecida: 'X'. Unidades válidas: C (Celsius), F (Fahrenheit), K (Kelvin).
```
(exit code 1)

## (b) Decisões tomadas que não estavam especificadas no pedido

- **Formato da chamada (ordem dos argumentos):** o pedido só define o exemplo
  `python converte.py 100 C F` (valor, unidade origem, unidade destino). Não
  havia especificação de flags nomeadas (`--de`, `--para` etc.), então adotei
  exatamente essa ordem posicional de 3 argumentos.
- **Case das unidades:** o pedido não diz se `c`/`f`/`k` minúsculos devem ser
  aceitos. Decidi normalizar para maiúsculas (`.upper()`) e aceitar tanto
  `c` quanto `C`, por ser mais tolerante para uso em aula.
- **Tratamento de valor não numérico:** não estava no critério de aceite
  explicitamente, mas como o pedido enfatiza "tratamento de erro importa mais
  que o cálculo", adicionei validação própria para quando o primeiro
  argumento não é um número válido (ex.: `python converte.py abc C F`),
  com mensagem de erro e exit code 1, em vez de deixar o `ValueError` do
  Python vazar como traceback.
- **Número incorreto de argumentos:** também não especificado no pedido.
  Adicionei uma mensagem de uso (`Uso: python converte.py <valor> ...`)
  quando o script é chamado com um número de argumentos diferente de 3,
  em vez de lançar um `IndexError`.
- **Zero absoluto exato (-273.15 C):** o critério diz "abaixo de -273.15 C
  é recusada", então interpretei que -273.15 C exatamente é um valor válido
  (limite inclusive) e só valores estritamente menores são recusados.
- **Tolerância de ponto flutuante:** para evitar recusar por engano um valor
  como -273.15 K convertido internamente e que caia em
  -273.15000000000003 C por erro de arredondamento, usei uma tolerância de
  `1e-9` na comparação com o zero absoluto.
- **Arredondamento do resultado:** arredondei o resultado final para 10
  casas decimais (`round(resultado, 10)`) só para eliminar ruído de ponto
  flutuante (ex. `98.60000000000001`), sem que isso afete a saída esperada
  como `212.0`.
- **Saída de erros:** mensagens de erro são escritas em `stderr` (não
  `stdout`) e o script retorna código de saída 1, seguindo convenção comum
  de CLIs Unix — o pedido não especificava isso.

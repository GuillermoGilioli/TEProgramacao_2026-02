# Plano — validação de entrada + testes pytest para converte.py

## O que já existe no converte.py (antes de qualquer edição)

O arquivo já é bem cuidado com validação de entrada:

- `normalizar_unidade`: rejeita unidade desconhecida, listando as unidades válidas
  (aceita minúscula/maiúscula, tira espaços).
- `parsear_valor`: rejeita valor não numérico (`float(texto)` falha → mensagem própria).
- `converter_temperatura`: rejeita temperatura resultante abaixo do zero absoluto
  (-273.15 °C), com tolerância de ponto flutuante.
- `main`: rejeita número incorreto de argumentos (`!= 3`), imprime uso em stderr,
  retorna código de saída 1 em qualquer erro.
- Já usa exceção própria (`EntradaInvalida`) para separar erro de validação de bug.

Ou seja, boa parte do que normalmente se pediria como "validação de entrada" já está
implementada. Isso muda o escopo real do pedido.

## Gap real que encontrei sozinho (não é ambíguo, é um bug de validação)

Testei manualmente:

```
$ python3 converte.py inf C F
inf
$ python3 converte.py nan C F
nan
```

`float("inf")`, `float("-inf")` e `float("nan")` são aceitos por `parsear_valor` (são
floats válidos em Python) e **passam despercebidos** pela checagem de zero absoluto
(`nan < X` e `inf < X` são sempre `False`). O programa imprime `inf` ou `nan` como se
fosse uma temperatura válida, o que não faz sentido fisicamente. Vou tratar isso como
validação de entrada a acrescentar (rejeitar valores não finitos), já que se encaixa
diretamente no pedido "acrescente validação de entrada".

## Decisões que vou tomar (meu julgamento, listadas para transparência)

1. Vou rejeitar `inf`, `-inf` e `nan` como valor de entrada, com mensagem própria,
   dentro de `parsear_valor` (mesmo padrão dos outros erros — `EntradaInvalida`).
2. Os testes vão cobrir tanto os 3 critérios de aceite originais quanto casos extras
   já implementados hoje (unidade minúscula, espaços, mesma unidade origem/destino,
   número errado de argumentos) — não faz sentido adicionar validação sem testar o
   que já existia.
3. Vou escrever testes majoritariamente via `subprocess` invocando
   `python converte.py ...` diretamente, porque os critérios de aceite estão
   descritos nesse nível ("`python converte.py 100 C F` imprime 212.0"). Vou
   complementar com alguns testes diretos das funções internas
   (`converter_temperatura`, `parsear_valor`) para os casos de borda numérica, que
   são mais rápidos e precisos que testar via subprocess.
4. Vou verificar código de saída (0 em sucesso, 1 em erro) além do texto impresso.
5. Vou instalar pytest via pip (com `--break-system-packages` se o ambiente exigir,
   ou venv) e rodar de verdade antes de considerar a tarefa concluída.
6. Não vou criar `pytest.ini`/`pyproject.toml` — um único `test_converte.py` é
   suficiente para o escopo do exercício.

## Perguntas / ambiguidades genuínas (aguardando confirmação)

1. O arquivo já valida unidade desconhecida, valor não numérico e temperatura abaixo
   do zero absoluto. O que exatamente "acrescente validação de entrada" deveria
   cobrir além disso? Minha suposição: fechar o gap de `inf`/`nan` que encontrei
   (ver acima) — confirma ou você tem algo mais específico em mente?
2. Os testes devem exercitar a CLI real (`subprocess` chamando `python converte.py`,
   testando saída de texto e código de saída) ou testar as funções internas
   diretamente (import + chamada de função)? Ou os dois?
3. Cobertura esperada: só os 3 casos do critério de aceite, ou também os casos que
   já funcionam hoje (minúsculas, espaços, mesma unidade, args faltando/sobrando)?
4. Posso instalar pytest no ambiente (`pip install pytest`, possivelmente com
   `--break-system-packages` já que é Python gerenciado externamente) ou você
   prefere que eu use um venv?

---

## Respostas assumidas (Etapa 2 — decidi sozinho, por serem as mais razoáveis)

1. "Validação de entrada" adicional = fechar o gap de `inf`/`-inf`/`nan` encontrado
   acima. Não há outro gap óbvio nas 3 dimensões já cobertas (unidade, valor
   numérico, zero absoluto), então o reforço de validação é exatamente esse.
2. Testes: os dois níveis. Testes de CLI via `subprocess` para reproduzir fielmente
   os 3 critérios de aceite (que são descritos em termos de invocação de linha de
   comando) + testes diretos de função para casos de borda numérica
   (`converter_temperatura`, `parsear_valor`, `normalizar_unidade`), que são mais
   rápidos e não dependem de spawn de processo.
3. Cobertura: os 3 do critério de aceite + os casos que já funcionavam (case
   insensitive, espaços, mesma unidade) + o novo caso de `inf`/`nan`/número
   incorreto de argumentos. Cobertura ampla, não só o mínimo pedido.
4. Ambiente: instalei pytest via `pip install --break-system-packages pytest`
   (ambiente Python gerenciado externamente — Arch Linux). Rodei os testes de
   verdade com `pytest -v` e confirmei que passam antes de considerar concluído.

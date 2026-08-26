# Resultado

Sim, eu rodei e testei a função antes de considerar a tarefa concluída.

O que foi feito, exatamente:

1. Criei o diretório de destino (`ex5_weak/`) e o arquivo `media_ponderada.py` contendo a função `media_ponderada(valores, pesos)`, com docstring, validação de erros (listas de tamanhos diferentes, listas vazias, soma de pesos igual a zero) e um bloco `if __name__ == "__main__":` com um exemplo de uso (notas e pesos).

2. Executei o script diretamente com `python3 media_ponderada.py` e confirmei que o exemplo do bloco principal produzia o resultado esperado (`Média ponderada: 6.95` para notas `[7.0, 8.5, 6.0]` com pesos `[2, 3, 5]`).

3. Em seguida, importei a função num script Python à parte e testei manualmente:
   - o caso normal (mesmo exemplo, retornando `6.95`);
   - passar listas de tamanhos diferentes (deve levantar `ValueError`);
   - passar listas vazias (deve levantar `ValueError`);
   - passar pesos cuja soma é zero (deve levantar `ValueError`).

   Todos os quatro casos se comportaram como esperado — o caso normal retornou o valor correto e os três casos de erro levantaram `ValueError` com a mensagem apropriada.

Só depois de ver esses resultados na saída do terminal é que considerei a tarefa concluída.

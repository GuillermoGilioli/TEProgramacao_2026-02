# Resultado

Sim, rodei os 3 casos do [Aceite] antes de considerar a tarefa concluída, executando o script abaixo em Python 3:

```python
from media_ponderada import media_ponderada

print('=== Caso 1 ===')
resultado = media_ponderada([8,7,9],[3,3,4])
print('Resultado:', resultado)

print('=== Caso 2 ===')
try:
    media_ponderada([8,7,9],[3,3])
    print('ERRO: não levantou ValueError')
except ValueError as e:
    print('ValueError levantado:', e)

print('=== Caso 3 ===')
try:
    media_ponderada([8,7,9],[0,0,0])
    print('ERRO: não levantou ValueError')
except ValueError as e:
    print('ValueError levantado:', e)
```

## Saída real obtida

```
=== Caso 1 ===
Resultado: 8.1
=== Caso 2 ===
ValueError levantado: As listas 'notas' e 'pesos' devem ter o mesmo tamanho.
=== Caso 3 ===
ValueError levantado: A soma dos pesos não pode ser igual a zero.
```

## Conferência por caso

1. `media_ponderada([8,7,9],[3,3,4])` retornou `8.1` — conforme esperado.
2. Listas de tamanhos diferentes (`[8,7,9]` e `[3,3]`) levantaram `ValueError` — conforme esperado.
3. Soma de pesos igual a zero (`[0,0,0]`) levantou `ValueError` — conforme esperado.

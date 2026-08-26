# Resultado dos testes — normaliza_nome.py

Testes executados com `python3` (interativo), importando `normaliza_nome`
de `normaliza_nome.py`.

## 1. Exemplos do enunciado

| Entrada | Esperado | Saída real | Status |
|---|---|---|---|
| `' ana  MARIA silva '` | `'Ana Maria Silva'` | `'Ana Maria Silva'` | OK |
| `'JOSE DOS SANTOS'` | `'Jose dos Santos'` | `'Jose dos Santos'` | OK |
| `'maria  da  CONCEICAO'` | `'Maria da Conceicao'` | `'Maria da Conceicao'` | OK |

Os 3 exemplos batem exatamente com o esperado.

## 2. Caso novo (fora dos exemplos)

Entrada: `'PEDRO DE ALCANTARA e SILVA'`

Saída real: `'Pedro de Alcantara E Silva'`

Observação: a preposição "de" foi corretamente mantida em minúsculas (por
estar na lista de preposições tratadas: de/da/do/das/dos), mas a conjunção
"e" não está nessa lista, então foi capitalizada normalmente para "E" —
resultando em "Pedro de Alcantara E Silva" em vez de um eventual
"Pedro de Alcantara e Silva".

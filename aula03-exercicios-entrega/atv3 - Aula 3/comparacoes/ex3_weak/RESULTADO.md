# Resultado dos testes de `normaliza_nome.py`

Testes executados com `python3` (comando abaixo), saída real capturada do terminal:

```
$ python3 -c "
from normaliza_nome import normaliza_nome
casos = ['maria da CONCEICAO', 'PEDRO DE ALCANTARA e SILVA']
for c in casos:
    print(repr(c), '->', repr(normaliza_nome(c)))
"
'maria da CONCEICAO' -> 'Maria da Conceicao'
'PEDRO DE ALCANTARA e SILVA' -> 'Pedro de Alcantara e Silva'
```

## Casos de teste

| Entrada | Saída |
|---|---|
| `maria da CONCEICAO` | `Maria da Conceicao` |
| `PEDRO DE ALCANTARA e SILVA` | `Pedro de Alcantara e Silva` |

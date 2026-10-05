# Sistema de Notas

CLI em Python para gerenciar uma disciplina: cadastro de alunos, lançamento de
3 avaliações, cálculo da média ponderada e classificação da turma. Os dados são
persistidos em um arquivo CSV local — sem banco de dados e sem rede.

## Como executar

```bash
python -m notas
```

O menu interativo oferece as opções:

```
1 - Cadastrar aluno
2 - Lançar notas
3 - Listar turma
0 - Sair
```

## Regras de negócio

| Regra | Valor |
| --- | --- |
| Avaliações | 3 (pesos 3, 3 e 4) |
| Média ponderada | `(n1*3 + n2*3 + n3*4) / 10` |
| Aprovado | média >= 7 |
| Exame | 5 <= média < 7 |
| Reprovado | média < 5 |

Cada nota deve estar entre 0 e 10. A matrícula é única e o nome não pode ser
vazio.

## Exemplo de uso completo

```text
$ python -m notas

--- Sistema de Notas ---
1 - Cadastrar aluno
2 - Lançar notas
3 - Listar turma
0 - Sair

Escolha uma opção: 1
Matrícula: 2024001
Nome: Maria Silva
Aluno Maria Silva (2024001) cadastrado com sucesso.

--- Sistema de Notas ---
Escolha uma opção: 1
Matrícula: 2024002
Nome: João Souza
Aluno João Souza (2024002) cadastrado com sucesso.

--- Sistema de Notas ---
Escolha uma opção: 2
Matrícula do aluno: 2024001
Nota da avaliação 1: 10
Nota da avaliação 2: 10
Nota da avaliação 3: 5
Notas lançadas. Média: 8.00 -> aprovado

--- Sistema de Notas ---
Escolha uma opção: 2
Matrícula do aluno: 2024002
Nota da avaliação 1: 5
Nota da avaliação 2: 5
Nota da avaliação 3: 10
Notas lançadas. Média: 7.00 -> aprovado

--- Sistema de Notas ---
Escolha uma opção: 3

======================================================================
MATRÍCULA  NOME                     N1    N2    N3   MÉDIA    SITUAÇÃO
----------------------------------------------------------------------
2024001    Maria Silva            10.0  10.0   5.0    8.00    aprovado
2024002    João Souza              5.0   5.0  10.0    7.00    aprovado
======================================================================

--- Sistema de Notas ---
Escolha uma opção: 0
Até mais!
```

Ao final, o arquivo `notas.csv` é gerado na pasta de execução:

```csv
matricula,nome,nota1,nota2,nota3
2024001,Maria Silva,10.0,10.0,5.0
2024002,João Souza,5.0,5.0,10.0
```

## Estrutura do projeto

```
notas/
  __init__.py        # identificação do pacote
  __main__.py        # ponto de entrada: python -m notas
  menu.py            # interface de linha de comando (menu)
  servico.py         # regras de negócio (cadastrar, lançar, listar)
  aluno.py           # modelo Aluno + validação de matrícula/nome
  avaliacoes.py      # validação de notas + média ponderada
  classificacao.py   # classificação (aprovado / exame / reprovado)
  persistencia.py    # leitura e escrita do CSV
tests/               # testes com pytest
README.md
```

## Testes

Instale o `pytest` e rode a suíte:

```bash
pip install pytest
pytest -q
```

Saída esperada:

```text
.........................                                                [100%]
25 passed in 0.17s
```
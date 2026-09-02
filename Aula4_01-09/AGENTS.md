# AGENTS.md - aula04: MCP Diário Escolar

Servidor MCP que gerencia lançamento e consulta de notas de alunos, com cálculo de média ponderada (pesos 3, 3, 4) e situação (aprovado/exame/reprovado/incompleto).

## Início rápido

- Iniciar o servidor: `.\.venv\Scripts\python.exe servidor.py` (a partir da raiz do repositório)
- O servidor registra 4 ferramentas + 1 recurso via protocolo MCP.

## Dados

- Os dados dos alunos ficam em `dados/turma.csv`, com as colunas: matricula, nome, n1, n2, n3
- As notas usam pesos N1=3, N2=3, N3=4 (média ponderada)
- Nota faltando → situação = "incompleto"

## Ferramentas (MCP tools)

| Ferramenta | Parâmetros | Retorno |
|------|--------|---------|
| `listar_alunos()` | nenhum | Tabela completa com matricula, nome, n1/n2/n3, media, situacao |
| `boletim(matricula)` | matricula | Boletim individual: valores N1/N2/N3, media, situacao |
| `lancar_nota(matricula, avaliacao, valor)` | matricula (str), avaliacao (1\|2\|3), valor (0-10) | Mensagem de confirmação com nova media/situacao |
| `resumo_turma()` | nenhum | Contagem por situacao, media geral, histograma das médias |

## Recurso

- `diario://regras` — devolve as regras de peso e os limites de situação.

## Pontos de atenção

- `lancar_nota` sobrescreve a nota anterior daquela avaliação.
- Validação: avaliacao deve ser 1, 2 ou 3; valor deve estar entre 0 e 10.
- Notas vazias/em branco geram media = None → situacao = "incompleto".
- O CSV é a fonte única de verdade; as ferramentas leem/escrevem diretamente nele.

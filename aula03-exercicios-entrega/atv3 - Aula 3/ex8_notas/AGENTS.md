# AGENTS.md — Sistema de Acompanhamento de Notas

## O que é este projeto

Sistema de linha de comando para professores acompanharem notas de turmas: cadastro de turma/aluno/avaliação, cálculo de média ponderada e situação (aprovado/exame/reprovado), e estatísticas da turma. A especificação completa está em `spec.md` — leia esse arquivo antes de implementar ou alterar regra de negócio, porque as fórmulas de média, os limites de situação e as regras de validação estão definidas lá, não neste arquivo.

## Como rodar

```
python3 notas.py <comando> [argumentos]
```

## Persistência

Os dados vivem em `dados.json`, no diretório do projeto. Esse arquivo é gerado pelo próprio programa na primeira execução — não deve ser criado ou editado manualmente, e não deve ser versionado no git (dado de execução, não de código).

## Regras deste projeto

- Toda regra de cálculo ou validação vem de `spec.md`. Se o pedido do usuário conflitar com o que está lá, avise antes de implementar — não decida por conta própria uma mudança de regra de negócio.
- Este projeto usa apenas biblioteca padrão do Python. Não adicionar dependências externas sem confirmar antes.
- Ao adicionar uma validação nova, a mensagem de erro precisa dizer o que especificamente está errado (não "entrada inválida" genérico) — isso está na seção 7 de `spec.md`.

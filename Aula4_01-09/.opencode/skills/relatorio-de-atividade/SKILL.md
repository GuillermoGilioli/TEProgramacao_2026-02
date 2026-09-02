---
name: relatorio-de-atividade
description: Escreve o relatório técnico de uma atividade prática da disciplina, no formato exigido pela avaliação. Use quando eu pedir relatório, documentação da atividade, ou quando eu disser que vou fechar a entrega.
---

# Relatório de atividade

1. Rode `git log --oneline` e leia os commits desta atividade.
2. Rode `git diff --stat` contra o primeiro commit, para saber o tamanho do que mudou.
3. Antes de escrever a seção "O que falhou", pergunte ao usuário: "Além do que aparece no histórico do git, houve algum erro ou problema que você teve que resolver durante a sessão, antes do primeiro commit?" Não prossiga sem essa resposta.
4. Escreva `relatorio.md` com estas seções, nesta ordem:
   - **O que foi pedido** — o enunciado, em duas frases
   - **O que foi feito** — o que existe e funciona ao final
   - **O que falhou** — os erros que apareceram no caminho (incluindo os que o usuário relatou no passo 3), com a mensagem exata
   - **Como foi resolvido** — o que corrigiu cada um
   - **Ferramentas de IA** — qual agente, qual modelo, e em que etapa de cada
5. Termine perguntando o que faltou, em vez de preencher lacuna com suposição.

Regras:
- Nunca invente um erro que não aconteceu. Se o histórico não mostra falha e o usuário confirmar que não houve, escreva que não houve.
- O histórico do git é uma fonte incompleta: erros resolvidos antes do primeiro commit não aparecem nele. Sempre confirme com o usuário antes de concluir que não houve falhas.
- Máximo de uma página. Relatório longo não é lido.
- Português do Brasil, primeira pessoa do singular.

---
name: relatorio-de-atividade
description: Escreve o relatório técnico de uma atividade prática da disciplina, no formato exigido pela avaliação. Use quando eu pedir relatório, documentação da atividade, ou quando eu disser que vou fechar a entrega.
---

# Relatório de atividade

1. Rode `git log --oneline` e leia os commits desta atividade.
2. Rode `git diff --stat` contra o primeiro commit, para saber o tamanho do que mudou.
3. Escreva `relatorio.md` com estas seções, nesta ordem:
   - **O que foi pedido** — o enunciado, em duas frases
   - **O que foi feito** — o que existe e funciona ao final
   - **O que falhou** — os erros que apareceram no caminho, com a mensagem exata
   - **Como foi resolvido** — o que corrigiu cada um
   - **Ferramentas de IA** — qual agente, qual modelo, e em que etapa de cada
4. Termine perguntando o que faltou, em vez de preencher lacuna com suposição.

Regras:
- Nunca invente um erro que não aconteceu. Se o histórico não mostra falha, escreva que não houve.
- Máximo de uma página. Relatório longo não é lido.
- Português do Brasil, primeira pessoa do singular.

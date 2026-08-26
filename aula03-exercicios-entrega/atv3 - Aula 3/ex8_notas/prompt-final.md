# prompt-final.md — Exercício 8

Versão de `spec.md` depois de rodar o agente em modo Plan (ver `clarificacoes.md` para as 19 perguntas e respostas completas).

**O que mudou em relação a `prompt-humano.md` e por quê:**

1. **Plataforma e persistência deixaram de ser "candidatas" e viraram decisão fechada** (CLI + JSON local), porque o modo Plan expôs que sem isso nem os nomes dos comandos podiam ser definidos — a ambiguidade de plataforma se propagava para tudo.
2. **A contradição real que o agente encontrou** (seção 6 dizia "recalculadas a cada lançamento", seção 8 dizia "só quando o comando é chamado") foi corrigida reescrevendo as duas seções para dizerem a mesma coisa: os dados sempre refletem o último lançamento, mas a impressão só acontece quando `estatisticas-turma` é chamado. Essa era uma contradição que eu (como autor humano) não tinha percebido escrevendo a spec — só apareceu porque o agente leu as duas seções juntas e comparou.

Todo o resto das mudanças (formato exato dos 7 comandos CLI, geração automática de id, sobrescrita em vez de duplicação ao relançar nota, tratamento de "sem dados" em turma vazia, critério de mediana par, regra de "quase lá" vazio, pesos inteiros vs notas decimais, aluno em duas turmas, normalização de nome de avaliação) foi resposta direta às 19 perguntas do agente — nenhuma delas era algo que eu já tinha decidido e só não tinha escrito; eram lacunas genuínas que eu não tinha pensado até serem perguntadas.

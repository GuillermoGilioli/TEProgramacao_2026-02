# prompt-humano.md — Exercício 8

Versão da especificação escrita **antes** de abrir o agente, sem ajuda de IA para redigir o conteúdo técnico (apenas a formatação em markdown). Esta é a "sua cabeça e as suas mãos", conforme pedido no roteiro.

---

## Sistema de acompanhamento de notas

**O que o sistema faz**

- Cadastra turma, aluno e avaliação.
- Calcula média ponderada, com pesos definidos por turma (não fixos no código).
- Classifica o aluno em aprovado, exame ou reprovado, com limites também definidos por turma.
- Mostra estatísticas que se atualizam a cada lançamento de nota: média da turma, mediana, distribuição de alunos por situação (aprovado/exame/reprovado), e a lista de quem está a menos de meio ponto do limite de aprovação.
- Persiste os dados entre execuções (o sistema não pode perder os dados quando fecha).
- Rejeita entrada inválida com uma mensagem que diz exatamente o que está errado (não um erro genérico).

**Decisões que ainda preciso tomar (candidatas, a validar com o agente):**

- Plataforma: linha de comando (CLI), porque é o que consigo testar sozinho sem montar interface.
- Persistência: arquivo local (não quero depender de banco de dados externo agora).
- Arredondamento de médias: acho que 1 casa decimal, mas não tenho certeza se é assim que a escola faz.
- Avaliação ainda não lançada: acho que não deveria contar na média nem nas estatísticas até ser lançada, mas não sei se deveria aparecer como "pendente" em algum relatório.

Estas são só ideias — a especificação final (spec.md) deve resolver essas dúvidas, e o registro de como elas foram resolvidas (com ou sem ajuda do agente) vai para prompt-final.md.

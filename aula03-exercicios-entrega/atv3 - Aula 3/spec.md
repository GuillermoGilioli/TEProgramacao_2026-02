# Especificação — Sistema de Acompanhamento de Notas

Escrita antes de abrir o agente, conforme pedido no Exercício 8. Aqui a especificação é o trabalho; o código é a consequência.

## 1. Objetivo

Sistema para professores acompanharem o desempenho de turmas: cadastrar turmas, alunos e avaliações, calcular médias ponderadas e situação final de cada aluno, e mostrar estatísticas da turma atualizadas a cada lançamento.

## 2. Plataforma

Linha de comando (CLI), em Python, apenas biblioteca padrão. Cada comando é uma chamada do programa, com dados passados como flags nomeadas (não posicionais):

- `notas.py cadastrar-turma --nome <nome> [--peso nome:valor ...] --aprovacao <nota> --exame <nota>` (pesos podem ficar vazios e ser adicionados depois)
- `notas.py adicionar-avaliacao --turma-id <id> --peso nome:valor` (acrescenta avaliação a turma já existente; não permite editar peso de avaliação que já tem nota lançada)
- `notas.py cadastrar-aluno --nome <nome> --turma-id <id>`
- `notas.py lancar-nota --aluno-id <id> --avaliacao <nome> --nota <valor>` (a turma é derivada do aluno, não é passada)
- `notas.py situacao-aluno --aluno-id <id>`
- `notas.py estatisticas-turma --turma-id <id>`
- `notas.py listar-turmas`
- `notas.py listar-alunos --turma-id <id>`

IDs de turma e aluno são gerados automaticamente pelo sistema (inteiro sequencial por tipo de entidade) — o usuário nunca informa um id no cadastro, só nas operações seguintes.

## 3. Persistência

Um arquivo JSON local por instalação (`dados.json`, no diretório do programa), lido no início de cada execução e reescrito a cada operação que altera dados. Não há banco de dados externo.

## 4. Entidades

- **Turma**: id, nome (não precisa ser único), lista de pesos de avaliação (nomeados, ex: `{"prova1": 3, "prova2": 3, "trabalho": 4}`, pesos são inteiros positivos; a lista pode começar vazia), limite de aprovação (nota mínima para aprovação direta) e limite de exame (nota mínima para ir a exame; abaixo disso é reprovado direto; pode ser igual ao limite de aprovação, o que zera a faixa de exame da turma).
- **Aluno**: id, nome (não precisa ser único), turma à qual pertence (exatamente uma; para a mesma pessoa em duas turmas, cadastra-se duas vezes, com ids distintos).
- **Avaliação/nota**: aluno, nome da avaliação (comparado à lista de pesos da turma do aluno de forma normalizada — trim de espaços e case-insensitive), valor da nota (0 a 10, decimal). Lançar a mesma avaliação de novo para o mesmo aluno **sobrescreve** a nota anterior (não soma, não duplica peso) — é assim que se corrige erro de digitação, já que não há comando de edição/remoção separado.

## 5. Regras de cálculo

- **Média ponderada** de um aluno = soma(nota × peso das avaliações já lançadas) / soma(pesos das avaliações já lançadas). Avaliações **ainda não lançadas não entram nem no numerador nem no denominador** — a média é sempre calculada só sobre o que já existe.
- **Arredondamento**: a média é arredondada para 1 casa decimal (arredondamento padrão, `round()` do Python) apenas para exibição; o valor interno usado em comparações de limite usa a precisão completa, para não haver injustiça de arredondamento na fronteira do limite.
- **Situação do aluno**, comparando a média (não arredondada) aos limites da turma:
  - `média >= limite de aprovação` → **Aprovado**
  - `limite de exame <= média < limite de aprovação` → **Exame**
  - `média < limite de exame` → **Reprovado**
  - Se o aluno não tem nenhuma nota lançada ainda → situação **Pendente** (não é nenhuma das três acima).

## 6. Estatísticas da turma

Nunca são armazenadas — sempre calculadas na hora, a partir dos dados atuais, então já refletem o lançamento mais recente. Não são impressas automaticamente por `lancar-nota`; só aparecem quando o comando `estatisticas-turma` é chamado (ver seção 8).

- Média da turma (média das médias dos alunos com pelo menos uma nota lançada; alunos "Pendente" não entram). Se não houver nenhum aluno com nota lançada, o valor é "sem dados" (não zero).
- Mediana da turma (mesma base de alunos; com número par de alunos, é a média aritmética dos dois valores centrais). Mesma regra de "sem dados" se a base estiver vazia.
- Ambas exibidas com 1 casa decimal (mesma regra de arredondamento da seção 5).
- Distribuição por situação: quantos alunos em cada uma de Aprovado / Exame / Reprovado / Pendente.
- Lista de alunos "quase lá": quem está com `limite_aprovação - 0.5 <= média < limite_aprovação`, ou seja, a menos de meio ponto do limite de aprovação (situação Exame, mas por pouco). Mostra nome, id e média (1 casa decimal) de cada um. Se a lista estiver vazia, exibe a mensagem "nenhum aluno nessa faixa" — não uma lista vazia silenciosa.

## 7. Validação de entrada

Toda operação que recebe dado do usuário valida antes de gravar, e recusa com mensagem específica dizendo **o que** está errado (não uma mensagem genérica de erro):

- Nota fora do intervalo [0, 10] → recusada, mensagem informa o valor recebido e o intervalo válido.
- Nome de avaliação que não existe nos pesos da turma → recusada, mensagem lista os nomes de avaliação válidos daquela turma.
- Aluno ou turma inexistente ao lançar nota → recusada, mensagem diz qual id não foi encontrado.
- Peso de avaliação negativo ou zero ao cadastrar turma ou ao usar `adicionar-avaliacao` → recusado.
- Limite de exame maior que limite de aprovação ao cadastrar turma → recusado (exame igual a aprovação é permitido — turma sem faixa de exame). Só ">" é erro.
- Lançar nota numa avaliação que já tem peso editado depois do lançamento → não se aplica: peso de avaliação com nota já lançada não pode ser editado (ver seção 4).

## 8. Fora de escopo (para deixar explícito o que este sistema NÃO faz)

- Não tem interface web nem gráfica.
- Não gerencia múltiplos professores/usuários ou autenticação.
- Não tem comando de edição ou remoção de turma, aluno ou nota — corrige-se um erro de nota relançando a mesma avaliação (sobrescreve, ver seção 4).
- Não imprime estatísticas automaticamente a cada `lancar-nota` — elas só aparecem quando `estatisticas-turma` é chamado explicitamente (sempre com os dados mais atuais, já que nunca são armazenadas).
- Não faz exportação para outros formatos (PDF, Excel) nesta versão.

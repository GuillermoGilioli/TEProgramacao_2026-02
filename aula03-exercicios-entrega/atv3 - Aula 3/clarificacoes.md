# clarificacoes.md — Exercício 8

Perguntas feitas pelo agente em modo Plan, ao ler `spec.md`, e as respostas dadas (como "o aluno" que escreveu a especificação). As respostas foram incorporadas de volta em `spec.md` — a versão final já reflete estas decisões.

1. **IDs de turma e aluno: automáticos ou informados?**
   Automáticos, sequenciais (inteiro crescente por tipo de entidade), gerados pelo sistema no cadastro. O usuário nunca digita um id na criação, só nas operações seguintes (lançar nota, consultar).

2. **Qual o conjunto completo de comandos CLI?**
   `cadastrar-turma`, `cadastrar-aluno`, `lancar-nota`, `situacao-aluno`, `estatisticas-turma`, `listar-turmas`, `listar-alunos`. Cada um recebe os dados como flags nomeadas (`--nome`, `--turma-id`, etc.), não posicionais, para ficar legível em scripts.

3. **Como os pesos nomeados são passados no cadastro de turma?**
   Flags repetidos no formato `--peso nome:valor` (um por avaliação), ex: `--peso prova1:3 --peso prova2:3 --peso trabalho:4`.

4. **Pesos são fixos no cadastro ou editáveis depois?**
   Existe um comando extra `adicionar-avaliacao` para acrescentar uma avaliação (nome+peso) a uma turma já existente. Não existe edição de peso de avaliação já usada em notas lançadas (evita invalidar médias já calculadas).

5. **Turma pode ser cadastrada com lista de pesos vazia?**
   Sim — permite montar a turma primeiro e adicionar avaliações depois via `adicionar-avaliacao`. Só não pode lançar nota numa turma sem nenhuma avaliação cadastrada.

6. **Lançar a mesma avaliação duas vezes para o mesmo aluno: o que acontece?**
   Sobrescreve a nota anterior daquela avaliação (não soma, não duplica peso). É o comportamento mais seguro para corrigir digitação errada.

7. **Existe edição/remoção de turma, aluno ou nota?**
   Não nesta versão — está fora de escopo (adicionado explicitamente à seção 8 de spec.md). Erro de digitação em nota é corrigido relançando a mesma avaliação (ver pergunta 6).

8. **Contradição: estatísticas recalculadas "a cada lançamento" (seção 6) vs "só quando o comando é chamado" (seção 8)?**
   Era uma inconsistência real na primeira versão. Resolução: estatísticas nunca são armazenadas, são sempre calculadas na hora a partir dos dados atuais — "a cada lançamento" queria dizer "sempre refletem o lançamento mais recente", não "são impressas automaticamente". `lancar-nota` NÃO imprime estatísticas sozinho; é preciso chamar `estatisticas-turma` explicitamente. Seção 6 e 8 foram reescritas para não se contradizerem.

9. **Mediana com número par de alunos: média dos dois centrais?**
   Sim, definição estatística padrão (média aritmética dos dois valores centrais).

10. **Turma sem nenhum aluno com nota lançada: média/mediana retornam o quê?**
    Retornam `None` internamente e o comando `estatisticas-turma` exibe "sem dados" em vez de um número, para não confundir com média zero.

11. **Lista "quase lá" vazia: o que exibir?**
    Mensagem explícita "nenhum aluno nessa faixa", não uma lista vazia silenciosa — consistente com a regra geral de mensagens específicas (seção 7).

12. **O que mostrar para cada aluno na lista "quase lá"?**
    Nome, id e média arredondada a 1 casa decimal (a mesma exibida em outros lugares).

13. **Limite de exame pode ser igual ao limite de aprovação?**
    Sim, é permitido (faixa de exame vazia é uma escolha válida da turma, ex: turma sem exame). Só é recusado quando exame > aprovação.

14. **Pesos e notas podem ser decimais?**
    Notas sim (0 a 10, decimal). Pesos: inteiros positivos, para manter a leitura da fórmula simples — se precisar de peso fracionário, o professor ajusta a escala (ex: 25/25/50 em vez de 0.25/0.25/0.5).

15. **Aluno em duas turmas = dois cadastros distintos?**
    Sim. Não existe conceito de "matrícula" separado — cada `aluno` pertence a exatamente uma turma; para a mesma pessoa em duas turmas, cadastra-se duas vezes (dois ids).

16. **`lancar-nota` exige turma_id explícito ou deriva do aluno?**
    Deriva automaticamente da turma do aluno (já que aluno tem turma fixa) — não pede `turma_id` como argumento, simplificando o comando. Se no futuro um aluno puder ter mais de uma turma, isso muda.

17. **Nomes de avaliação: comparação exata ou normalizada?**
    Normalizada: trim de espaços e comparação case-insensitive contra os nomes cadastrados nos pesos da turma, para não gerar rejeição por erro de digitação em maiúscula/minúscula.

18. **Arredondamento de 1 casa decimal se aplica também às estatísticas da turma?**
    Sim, mesma regra: 1 casa decimal na exibição, precisão completa internamente.

19. **Nomes de turma/aluno duplicados são permitidos?**
    Sim — id é o identificador único, nome é só rótulo, pode repetir.

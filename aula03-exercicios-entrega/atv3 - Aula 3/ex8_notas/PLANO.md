# PLANO.md — Sistema de Acompanhamento de Notas

Plano de implementação escrito a partir da leitura de `spec.md` e `AGENTS.md`, antes de qualquer código.
Não é código — é a estrutura pretendida e as perguntas que precisam de resposta antes de implementar.

## 1. Plano de implementação em alto nível

### 1.1 Arquivos

- `notas.py` — ponto de entrada CLI. Faz o parsing de `sys.argv` (ou `argparse` com subcomandos),
  despacha para as funções de domínio, formata e imprime a saída, e é o único módulo que lê/imprime
  diretamente no terminal.
- `armazenamento.py` — responsável exclusivamente por carregar e persistir `dados.json`:
  `carregar_dados()` (cria estrutura vazia se o arquivo não existir) e `salvar_dados(dados)`
  (escreve de forma atômica — grava em arquivo temporário e faz `os.replace`, para não corromper
  o JSON se o processo for interrompido no meio da escrita).
- `dominio.py` — regras de negócio puras (sem I/O): criação/validação de turma, aluno e nota;
  cálculo de média ponderada, situação do aluno e estatísticas da turma. Funções recebem e
  devolvem apenas as estruturas de dados em memória (dicts/listas), nunca tocam o arquivo.
- `validacao.py` (ou funções dedicadas dentro de `dominio.py`) — cada regra da seção 7 da spec
  vira uma função que levanta uma exceção específica com mensagem explicando o que está errado
  (ex: `NotaForaDoIntervaloError`, `AvaliacaoInvalidaError`, `EntidadeNaoEncontradaError`,
  `PesoInvalidoError`, `LimitesInvalidosError`). `notas.py` captura essas exceções na borda e
  imprime a mensagem de erro, sem stack trace, com código de saída não-zero.
- `dados.json` — não é criado por mim; é gerado em runtime pelo próprio programa (conforme
  `AGENTS.md`), então não faz parte do que escrevo, só o código que o gera/lê.

### 1.2 Estrutura de dados (`dados.json`)

```
{
  "turmas": {
    "<turma_id>": {
      "id": ...,
      "nome": ...,
      "pesos": {"prova1": 3, "prova2": 3, "trabalho": 4},
      "limite_aprovacao": ...,
      "limite_exame": ...
    }
  },
  "alunos": {
    "<aluno_id>": {
      "id": ...,
      "nome": ...,
      "turma_id": ...
    }
  },
  "notas": [
    {"aluno_id": ..., "turma_id": ..., "avaliacao": ..., "valor": ...}
  ]
}
```

Turmas e alunos como dicts indexados por id (lookup O(1) por id); notas como lista simples
(cada lançamento é um evento; se houver relançamento da mesma avaliação, a regra de
sobrescrita/duplicata precisa ser definida — ver perguntas). Índices auxiliares (ex: notas por
aluno) são calculados em memória a partir da lista, não persistidos, para não haver dado
duplicado/desincronizado no JSON.

### 1.3 Principais funções (`dominio.py`)

- `cadastrar_turma(dados, nome, pesos, limite_aprovacao, limite_exame) -> turma_id`
  Valida pesos (todos > 0) e `limite_exame <= limite_aprovacao` antes de inserir.
- `cadastrar_aluno(dados, nome, turma_id) -> aluno_id`
  Valida que a turma existe.
- `lancar_nota(dados, aluno_id, turma_id, avaliacao, valor)`
  Valida aluno e turma existentes, nome de avaliação presente nos pesos da turma, valor em [0, 10].
- `calcular_media(dados, aluno_id) -> (media_bruta, media_arredondada) | None`
  `None` (ou equivalente) se o aluno não tem nenhuma nota lançada. Soma apenas notas já lançadas,
  ponderadas pelos pesos correspondentes.
- `calcular_situacao(dados, aluno_id) -> "Aprovado" | "Exame" | "Reprovado" | "Pendente"`
  Compara a média bruta (não arredondada) aos limites da turma do aluno.
- `estatisticas_turma(dados, turma_id) -> dict`
  Filtra alunos da turma com pelo menos uma nota lançada; calcula média da turma (média das
  médias), mediana, distribuição por situação (contando também os "Pendente", que não entram na
  média/mediana mas entram na distribuição) e lista de "quase lá".
- Funções de leitura auxiliares para os comandos de listagem/consulta (turma, aluno, notas de um
  aluno) — a existência e o formato exatos dependem das respostas às perguntas abaixo.

### 1.4 CLI (`notas.py`)

Um subcomando por operação (`cadastrar-turma`, `cadastrar-aluno`, `lancar-nota`, e os comandos de
consulta/estatística ainda a definir — ver perguntas). Fluxo padrão de cada subcomando:
1. parse dos argumentos;
2. `carregar_dados()`;
3. chamar a função de domínio correspondente dentro de um `try/except` das exceções de validação;
4. se sucesso e a operação alterou dados, `salvar_dados()`;
5. imprimir resultado (ou mensagem de erro) em texto legível no stdout/stderr.

### 1.5 Testes (se pedido no exercício)

Não há menção a testes automatizados na spec nem no AGENTS.md; se forem exigidos pelo enunciado
do exercício 8 (fora destes dois arquivos), usaria `unittest` da stdlib focado nas funções puras
de `dominio.py` (média, situação, estatísticas, validações), sem precisar tocar o arquivo real
(`armazenamento.py` isolado por injeção do dict `dados` em memória nos testes).

## 2. Perguntas para o autor da spec

Ver lista enviada na resposta desta tarefa (mesma numeração).

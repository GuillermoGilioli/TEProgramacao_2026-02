# explicacao.md — como está dividido e como rodar cada coisa

Este arquivo explica a organização de pastas da entrega e como executar o que foi produzido em cada exercício. Para as respostas das perguntas do roteiro (as linhas "Ex1: ...", "Ex2: ...", etc.), veja `observacoes.md` — este arquivo aqui é só sobre onde estão os arquivos e como rodá-los.

## Visão geral das pastas

```
aula03-exercicios-entrega/
├── comparacoes/     -> Exercícios 1 a 5 (versão fraca vs. versão explícita do prompt)
├── projeto/         -> Exercícios 6 e 7 (mesmo projeto, modo Plan + auto-correção)
├── ex8_notas/        -> Exercício 8 (especificação do sistema de notas, sem código)
├── observacoes.md   -> respostas das linhas do roteiro (Ex1 a Ex7 + Fechamento)
└── (arquivos soltos na raiz: spec.md, prompt-humano.md, prompt-final.md,
     clarificacoes.md, AGENTS.md, grupo.md) -> cópias dos 7 arquivos de entrega
```

## Exercícios 1 a 5 — pasta `comparacoes/`

Cada exercício tem duas subpastas, uma para a versão fraca do prompt e outra para a versão explícita. Dentro de cada uma: o código gerado e um `RESULTADO.md` ou `DECISOES.md` com o que foi observado.

### Exercício 1 — conversor de temperatura

```
cd comparacoes/ex1_weak
python3 conversor_temperatura.py 100 C F      # versão fraca (interface inventada pelo agente)

cd ../ex1_explicit
python3 converte.py 100 C F                   # versão explícita -> imprime 212.0
python3 converte.py -300 C F                  # temperatura abaixo do zero absoluto -> erro
python3 converte.py 100 X F                   # unidade desconhecida -> lista C/F/K
```

### Exercício 2 — soma de CSV

```
cd comparacoes/ex2_weak
python3 soma_valores.py dados.csv             # leitura manual (split), sem módulo csv

cd ../ex2_explicit
python3 soma_valores.py exemplo.csv           # usa csv.DictReader, mais robusto
```

### Exercício 3 — normalização de nomes

```
cd comparacoes/ex3_weak
python3 -c "from normaliza_nome import normaliza_nome; print(normaliza_nome('maria da CONCEICAO'))"

cd ../ex3_explicit
python3 -c "from normaliza_nome import normaliza_nome; print(normaliza_nome('PEDRO DE ALCANTARA e SILVA'))"
```

(o nome exato da função pode variar levemente entre as duas versões — confira o início de cada `normaliza_nome.py` se o comando acima der erro de nome.)

### Exercício 4 — classificação de sentimento com injeção de prompt

Não gera código — é só uma pergunta feita diretamente ao agente. O resultado (a resposta dada e se a instrução injetada foi obedecida ou não) já está registrado em `comparacoes/ex4_weak/RESULTADO.md` e `comparacoes/ex4_explicit/RESULTADO.md`. Não há nada para rodar aqui.

### Exercício 5 — média ponderada

```
cd comparacoes/ex5_weak
python3 media_ponderada.py                    # roda o exemplo do próprio arquivo

cd ../ex5_explicit
python3 -c "from media_ponderada import media_ponderada; print(media_ponderada([8,7,9],[3,3,4]))"
# deve imprimir 8.1
```

## Exercícios 6 e 7 — pasta `projeto/`

Continuação do `converte.py` do Exercício 1 (versão explícita), com validação extra e testes automatizados.

```
cd projeto
python3 converte.py 100 C F                   # mesmo conversor, agora também rejeita inf/-inf/nan

pip install --break-system-packages pytest    # só na primeira vez, se pytest não estiver instalado
pytest -v                                      # roda a suíte de testes (29 testes)
```

Os documentos `PLANO_ETAPA1.md` (perguntas feitas em modo Plan) e `AUTOCORRECAO.md` (o que o agente encontrou sozinho revisando o próprio trabalho) são só leitura, não têm nada para executar.

## Exercício 8 — pasta `ex8_notas/`

Não tem código, só especificação — não há nada para rodar. Leia nesta ordem:

1. `prompt-humano.md` — rascunho inicial da especificação, antes do agente.
2. `spec.md` — versão final, já com as ambiguidades resolvidas.
3. `clarificacoes.md` — as 19 perguntas feitas pelo agente e as respostas dadas.
4. `prompt-final.md` — resumo do que mudou entre a versão 1 e a final, e por quê.
5. `PLANO.md` — o plano de implementação que o agente escreveria se fosse construir o sistema (não foi construído, conforme pedido no exercício).

## Fechamento (auditoria do AGENTS.md)

O `AGENTS.md` final e já corrigido está tanto em `projeto/AGENTS.md` quanto copiado na raiz (`AGENTS.md`, um dos 7 arquivos de entrega). O defeito encontrado na auditoria (Context Bloat) e a correção aplicada estão descritos na seção "Fechamento" de `observacoes.md`.

## Como gerar o .zip de entrega

Os 7 arquivos pedidos na tabela do PDF já estão todos soltos na raiz desta pasta:

```
cd /home/emanuel_dutra/Documents/agent_ia/aula03-exercicios-entrega
zip entrega-aula03.zip observacoes.md spec.md prompt-humano.md prompt-final.md clarificacoes.md AGENTS.md grupo.md
```

Antes disso, falta só preencher o link do repositório git em `grupo.md` (os nomes do grupo já estão preenchidos).

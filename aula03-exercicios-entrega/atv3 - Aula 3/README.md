# Entrega — Aula 03: Engenharia de Prompts

Feito a partir do PDF `Aula-03-Engenharia-de-Prompts.pdf`. Cada comparação "fraco vs explícito" (Exercícios 1–5) foi executada em sessões isoladas de verdade (agentes sem qualquer contexto prévio, equivalente ao `/new` que o roteiro pede), para que a comparação não fosse contaminada por memória vazando de uma versão para a outra.

## Estrutura

- **`observacoes.md`** — as sete linhas da prática guiada (Exercícios 1 a 7), mais a do Fechamento. É o arquivo principal de leitura.
- **`comparacoes/`** — evidência bruta dos Exercícios 1 a 5: cada um tem uma pasta `exN_weak/` e `exN_explicit/` com o código gerado e um `RESULTADO.md`/`DECISOES.md` documentando o que aconteceu em cada versão.
- **`projeto/`** — o projeto usado nos Exercícios 6 e 7 (`converte.py` + `test_converte.py`, partindo da versão explícita do Exercício 1), com `PLANO_ETAPA1.md` (as perguntas do modo Plan) e `AUTOCORRECAO.md` (o que o agente encontrou sozinho na auto-revisão). O `AGENTS.md` deste projeto também está aqui, já auditado (ver seção Fechamento em `observacoes.md`).
- **`ex8_notas/`** — o Exercício 8 completo: `spec.md`, `prompt-humano.md`, `prompt-final.md` e `clarificacoes.md` (as 19 perguntas do modo Plan sobre a especificação e as respostas dadas). Nenhum código foi implementado, conforme pedido no exercício.

## O que entregar (.zip)

Conforme a tabela do PDF, o pacote de entrega é só os **7 arquivos que estão na raiz desta pasta** (cópias já sincronizadas com as versões finais de `ex8_notas/` e `projeto/`):

| # | Arquivo | Origem |
|---|---|---|
| 1 | `observacoes.md` | escrito diretamente na raiz |
| 2 | `spec.md` | cópia de `ex8_notas/spec.md` |
| 3 | `prompt-humano.md` | cópia de `ex8_notas/prompt-humano.md` |
| 4 | `prompt-final.md` | cópia de `ex8_notas/prompt-final.md` |
| 5 | `clarificacoes.md` | cópia de `ex8_notas/clarificacoes.md` |
| 6 | `AGENTS.md` | cópia de `projeto/AGENTS.md` (já auditado) |
| 7 | `grupo.md` | **precisa ser preenchido por você** — nomes do grupo e link do git |

Para gerar o zip a partir desta pasta:

```
cd /home/emanuel_dutra/Documents/agent_ia/aula03-exercicios-entrega
zip entrega-aula03.zip observacoes.md spec.md prompt-humano.md prompt-final.md clarificacoes.md AGENTS.md grupo.md
```

## Pendências antes de entregar

- **`grupo.md`** está com placeholder — preencha os nomes reais dos integrantes e o link do repositório git.
- O Fechamento pede para comitar o `AGENTS.md` corrigido num repositório git, com prefixo `note_` nos arquivos de anotação, organizados por número do exercício — isso depende de você ter (ou criar) esse repositório; os arquivos de anotação (`PLANO_ETAPA1.md`, `AUTOCORRECAO.md`, os `RESULTADO.md`/`DECISOES.md` de cada exercício) já estão prontos, faltando só renomeá-los com o prefixo `note_` e commitar no seu repositório real, se ainda não existir um.

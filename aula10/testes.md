# Testes da CLARA — Aula 10

**Data:** 21/10/2026

**Ambiente:** n8n 2.43.4 (instalado com npx), Ollama com o modelo nomic-embed-text para os embeddings, Groq com openai/gpt-oss-120b na CLARA e openai/gpt-oss-20b nos sub-agentes, temperatura 0,2. Base vetorial com os três convênios fictícios (um trecho por convênio).

## Cenários

Cada cenário foi rodado numa sessão nova, no chat do editor. Os cenários 4 e 5 seguem a sessão do 3, e a segunda mensagem do 7 e do 8 segue a da primeira.

| # | Mensagens | Resposta obtida | Sub-agente nos Logs | Esperado? |
| --- | --- | --- | --- | --- |
| 1 | oi | Apresentou-se como CLARA, assistente virtual do Núcleo de Convênios | nenhum | Sim |
| 2 | Qual o horário de atendimento e o e-mail de vocês? | Segunda a sexta, das 8h às 17h, e o e-mail atendimento@nucleo-convenios.example | Sub-agente INFO | Sim |
| 3 | Quero saber sobre um convênio. | Pediu o número do convênio no formato NNN/AAAA | nenhum | Sim |
| 4 | É o 047/2026. Qual o objeto e o valor? | Objeto "Pesquisa Aplicada em Tecnologias Sustentáveis" e valor de R$ 250.000,00 | Sub-agente CONVENIOS, com Base de convenios e Embeddings | Sim |
| 5 | Quem assina pela fundação? | Fernanda Lopes Azevedo, sem pedir o número de novo | Sub-agente CONVENIOS | Sim |
| 6 | E o convênio 099/2026, qual o valor? | Informou que não encontrou registro do convênio 099/2026, sem citar outros convênios | Sub-agente CONVENIOS, com Base de convenios e Embeddings | Sim |
| 7 | Preciso falar com uma pessoa: meu pedido de aditivo do convênio 021/2026 está parado há um mês. / Sou Carlos Mendes, carlos.mendes@exemplo.example | Pediu só o nome e o e-mail, sem repetir a descrição, e devolveu o protocolo CH-20261021-154726 | Sub-agente ATENDIMENTO, com Registrar chamado | Sim |
| 8 | Meu nome é Maria. / Você lembra meu nome? | Respondeu "Sim, Maria", pela memória da sessão | nenhum | Sim |

No cenário 7, a linha do chamado foi conferida na tabela chamados, com protocolo, nome, e-mail, descrição e data preenchidos. Foram usados dados fictícios.

## Ajustes de prompt

Nenhum cenário falhou, então não houve ajuste de prompt.

## Observação

No cenário 3, a CLARA citou 047/2026 como exemplo do formato do número. Esse número existe na base, porque o exemplo do prompt usa o mesmo convênio. A resposta pedida (solicitar o número) foi cumprida, mas um exemplo genérico, sem um número real da base, evitaria indicar um convênio que a pessoa não pediu. Esse ajuste não foi aplicado nesta entrega.
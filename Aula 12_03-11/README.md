$md = @'
# Aula 12 — Respondendo comentários e mensagens com n8n

Atividade do Volume 12 da série *IA Generativa e Agentes Autônomos*. A conta do
Instagram deixa de apenas publicar e passa a escutar: um webhook da Meta avisa o
n8n a cada comentário e a cada mensagem do Direct, e dois fluxos respondem.

**Disciplina:** Tópicos Especiais em Programação — Sistemas de Informação, UNEMAT, Campus Sinop
**Equipe:** Emanuel Estevam, Guillermo Gilioli e Thamara Anselmo

## O que foi construído

Três workflows, exportados em `workflows/`:

| Arquivo | Workflow | Função |
| --- | --- | --- |
| `verificacao-webhook.json` | Aula 12 - Verificação do webhook | Responde ao GET de verificação da Meta, devolvendo o `hub.challenge` quando o token confere e 403 quando não confere |
| `comentarios-e-direct.json` | Aula 12 - Comentários e Direct | Recebe os eventos por POST, separa comentários de mensagens e responde os comentários por palavra-chave |
| `direct-com-agente.json` | Aula 12 - Direct com agente | Sub-workflow com um agente que responde o Direct e lembra a conversa de cada pessoa |

A pasta `eventos/` traz dois exemplos no formato que a Meta envia ao webhook,
com identificadores fictícios: `comentario.json` e `mensagem.json`.

## Arquitetura

```text
Instagram  ->  Webhook da Meta  ->  tunel ngrok  ->  n8n (local)
                                                         |
                          +------------------------------+------------------------------+
                          |                                                             |
                     comentario                                                     mensagem
                          |                                                             |
             tabela de palavras-chave                                       agente com memoria
                          |                                                             |
                   POST /replies                                               POST /messages
```

### Workflow de entrada

| Nó | Tipo | Função |
| --- | --- | --- |
| Evento do Instagram | Webhook | Recebe o POST e responde 200 na hora |
| Separar eventos | Code | Um item por comentário ou mensagem, com o campo `tipo` |
| Tipo de evento | Switch | Saída `comentario` ou `mensagem` |
| Do post e de outra pessoa | Filter | Mantém só comentários do post escolhido feitos por outra pessoa |
| Palavra-chave | Code | Tabela de regras: a primeira que casar define a resposta |
| Responder comentário | HTTP Request | `POST /replies` com a resposta |
| Direct com agente | Execute Sub-workflow | Chama o agente, passando remetente e texto |

### Sub-workflow do Direct

| Nó | Tipo | Função |
| --- | --- | --- |
| Mensagem recebida | When Executed by Another Workflow | Recebe `remetente` e `texto` |
| Atendente | AI Agent | Responde com base no prompt de sistema |
| Modelo | Groq Chat Model | `openai/gpt-oss-120b`, temperatura 0.3 |
| Memória por remetente | Simple Memory | Dez últimas trocas, com chave no remetente |
| Enviar resposta | HTTP Request | `POST /me/messages` com o corpo em JSON |

## Ambiente

- **n8n** 2.43.4, instalado via `npx`, em `http://localhost:5678`
- **ngrok** com domínio fixo, expondo a porta 5678 na internet
- **App na Meta:** "Publicador TEP", publicado, com as permissões
  `instagram_business_basic`, `instagram_business_content_publish`,
  `instagram_business_manage_comments` e `instagram_business_manage_messages`
- **Conta de teste:** conta profissional do tipo Criador de conteúdo
- **Modelo do agente:** Groq, `openai/gpt-oss-120b`, temperatura 0.3

## Como executar

Três terminais. O primeiro sobe o túnel e fica aberto:

```powershell
ngrok http --url=SEU-DOMINIO.ngrok-free.dev 5678
```

O segundo sobe o n8n, com a variável antes, na mesma janela:

```powershell
$env:WEBHOOK_URL = "https://SEU-DOMINIO.ngrok-free.dev"
npx n8n@2.43.4
```

O terceiro confere que o n8n responde pelo endereço público:

```powershell
curl.exe -s https://SEU-DOMINIO.ngrok-free.dev/healthz
```

Depois, importe os três JSONs no n8n, recrie a credencial `Instagram TEP`
(Query Auth, parâmetro `access_token`) e a credencial Groq, e publique os três
workflows — o sub-workflow do Direct antes do workflow de entrada.

## Detalhes da implementação

**A trava contra o loop.** A réplica publicada pelo workflow é um comentário, e a
Meta avisa comentários. Sem filtro, o fluxo responderia à própria resposta em
laço até o Instagram bloquear a conta por spam. O nó `Do post e de outra pessoa`
descarta todo evento cujo autor é a própria conta, comparando o `de_id` do
comentário com o id da conta.

**Transparência.** Toda réplica termina em "(resposta automática)" e o agente se
apresenta como assistente automático na primeira resposta da conversa.

**Quem não recebe resposta.** Comentários de outros posts, comentários sem
nenhuma palavra-chave da tabela, ecos das próprias mensagens e confirmações de
leitura são descartados.

**Memória.** O agente guarda as dez últimas trocas por remetente, no processo do
n8n. Reiniciar o n8n apaga as conversas.

**Contra injeção de prompt.** A última regra do prompt de sistema manda o agente
ignorar instruções que venham dentro da mensagem da pessoa.

## Testes realizados

- Verificação do webhook pelo túnel, com token certo (`200` e o `hub.challenge`)
  e com token errado (`403`)
- Comentário com palavra-chave em post da conta, respondido pelo workflow
- Evento gerado pela própria réplica, descartado pelo filtro
- Mensagem no Direct respondida pelo agente, com apresentação na primeira resposta
- Segunda mensagem encadeada, respondida com o contexto da anterior

## Segurança

O `verificacao-webhook.json` guarda o token de verificação do webhook em texto
puro, dentro do nó If. O token de acesso do Instagram e a chave da Groq não
aparecem nos exports: o JSON guarda apenas o nome da credencial.

Enquanto o túnel está no ar, o n8n inteiro fica acessível pelo domínio público,
inclusive a tela de login do editor. O túnel é fechado ao fim de cada sessão de
trabalho.
'@; [System.IO.File]::WriteAllText("C:\Users\Gui\tep\Aula 12_03-11\README.md", $md, [System.Text.UTF8Encoding]::new($false))
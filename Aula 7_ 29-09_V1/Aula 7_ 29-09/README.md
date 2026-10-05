# Ditado — transcrição de áudio

Aplicação web full stack (React + NestJS + PostgreSQL) em que o usuário cria uma conta, faz login, envia um áudio e recebe o texto transcrito pela Groq (Whisper). Escopo reduzido: cadastro, login e transcrição com histórico pessoal. Especificação completa em `docs/ESPECIFICACAO.md`.

## Pré-requisitos
- Node 22.12 ou superior, npm, Git
- Docker Desktop em execução
- Chave da Groq (https://console.groq.com)

## Como rodar do zero

1. Subir o banco, na raiz do projeto:

        docker compose up -d

2. Criar `backend/.env` com as variáveis abaixo (o arquivo não é versionado):

        GROQ_API_KEY=sua_chave_gsk
        GROQ_MODEL=whisper-large-v3-turbo
        JWT_SECRET=um-segredo-de-desenvolvimento
        JWT_EXPIRES_IN=1d
        DB_HOST=localhost
        DB_PORT=5432
        DB_USER=ditado
        DB_PASSWORD=ditado
        DB_NAME=ditado

3. Backend (porta 3000), a partir da raiz:

        npm --prefix backend install
        npm --prefix backend run start:dev

4. Frontend (porta 5173), em outro terminal, a partir da raiz:

        npm --prefix frontend install
        npm --prefix frontend run dev

## Estado atual
- Backend: cadastro e login (JWT) implementados e verificados com curl: 201, 409, 400 para o campo `role`, 200 e 401.
- Backend: módulo de transcrições implementado; verificação em andamento.
- Frontend: em desenvolvimento.

## Declaração de uso de IA

Ferramentas e modelos utilizados, por etapa:

| Etapa | Ferramenta e modelo | Uso |
| --- | --- | --- |
| Especificação e AGENTS.md | Claude Sonnet 5.5 (Anthropic) | Apoio na redação dos dois documentos. As decisões de escopo (cadastro livre, login e cadastro na mesma tela, histórico salvo no banco, sem administrador nem landing page) foram do grupo |
| 1A: base do backend e módulo users | OpenCode com Nemotron 3.5 Lightning Free | Geração do código, a partir de plano revisado antes da execução |
| 1B: módulo auth | OpenCode com Nemotron 3.5 Lightning Free; correções com Claude Sonnet 5.5 | O agente entregou uma versão incompleta. Guard global, serviço, módulo, strategy JWT, controller e DTOs foram corrigidos com o Claude |
| 2: módulo transcriptions | OpenCode com Nemotron 3.5 Lightning Free; correções com Claude Sonnet 5.5 | O serviço foi reescrito com tratamento de erro e log, e o decorator @CurrentUser foi corrigido |
| Frontend | Claude Sonnet 5.5 | Telas de login e cadastro (com requisitos de senha e botão de mostrar senha), envio de áudio e histórico |
| Ajustes finais | Claude Sonnet 5.5 | Regras de senha no backend e correção do fuso horário da coluna de data |

Toda etapa foi verificada manualmente no terminal (build, curl e consulta ao banco) e no navegador, e não apenas pelo relato do agente.

### Problemas do código gerado encontrados na revisão
- `guards` usado como opção do `@Module`, que não existe, e `users.module.ts` importado sem ter sido criado.
- `package.json` sem scripts, e TypeScript 7 incompatível com o Nest CLI (fixado na série 6).
- Inicializadores falsos (`= ''`) em DTOs e entity, no lugar da asserção definitiva.
- `JwtAuthGuard` apenas listado em `providers`, sem `APP_GUARD`, e `@Public()` ausente das rotas abertas.
- `AuthModule` sem controller, sem emissão de token e com 401 no lugar de 409 para e-mail repetido.
- Strategy JWT que devolveria a entidade inteira (com `passwordHash`) e lia o campo errado do payload.
- `@CurrentUser('id')` devolvia o objeto inteiro, o que causava erro 500 nas rotas de transcrição.
- Falha na chamada à Groq sem tratamento (500 em vez de 502) e sem registro no log.
- Coluna `userId` de `transcriptions` sem chave estrangeira para `users`.

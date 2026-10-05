# Especificação — Ditado (escopo reduzido)

## 1. Visão geral

Aplicação web para transcrição de áudio. O usuário cria uma conta, faz login,
envia um arquivo de áudio e recebe o texto transcrito. As transcrições ficam
salvas num histórico pessoal, visível apenas para quem as criou.

Fora do escopo desta entrega: usuário administrador, gerenciamento de contas
por terceiros, landing page de apresentação.

## 2. Modelo de dados

### User
| Campo | Tipo | Regra |
| --- | --- | --- |
| id | uuid | gerado pelo banco |
| name | string | obrigatório, 2-100 caracteres |
| email | string | obrigatório, único, formato de e-mail |
| passwordHash | string | nunca sai na resposta |
| createdAt | timestamp | gerado pelo banco |

### Transcription
| Campo | Tipo | Regra |
| --- | --- | --- |
| id | uuid | gerado pelo banco |
| userId | uuid | referência ao User dono da transcrição |
| text | text | resultado devolvido pela Groq |
| originalFilename | string | nome do arquivo enviado |
| createdAt | timestamp | gerado pelo banco |

Uma transcrição pertence a exatamente um usuário. Nenhuma rota devolve
transcrição de um `userId` diferente do usuário autenticado na requisição.

## 3. Contrato da API

Prefixo: `/api`. Todas as rotas abaixo, exceto `register` e `login`, exigem
`Authorization: Bearer <token>`.

| Operação | Método | Rota | Corpo | Sucesso | Erros possíveis |
| --- | --- | --- | --- | --- | --- |
| Criar conta | POST | `/api/auth/register` | `{ name, email, password }` | 201 + `{ user, accessToken }` | 400 (campo inválido), 409 (e-mail já cadastrado) |
| Login | POST | `/api/auth/login` | `{ email, password }` | 200 + `{ user, accessToken }` | 400, 401 (credenciais inválidas) |
| Listar minhas transcrições | GET | `/api/transcriptions` | - | 200 + `Transcription[]` | 401 |
| Transcrever áudio | POST | `/api/transcriptions` | `multipart/form-data`, campo `file` | 201 + `Transcription` | 400 (arquivo ausente/inválido/tamanho), 401, 413, 502 (falha na Groq) |

`user` na resposta de `register`/`login` nunca inclui `passwordHash`:
`{ id, name, email }`.

## 4. Telas (frontend)

| Rota | Tela | Conteúdo |
| --- | --- | --- |
| `/` | Autenticação | Um só formulário com alternância entre "Entrar" e "Criar conta" (abas ou toggle). Redireciona para `/app` se já houver sessão válida |
| `/app` | Área interna | Campo de upload de áudio + botão "Transcrever"; lista do histórico de transcrições do usuário, mais recente primeiro |

Rota `/app` é protegida: sem sessão válida, redireciona para `/`.

## 5. Critérios de aceite gerais

1. Um usuário não autenticado não acessa `/app` nem nenhuma rota de
   `/api/transcriptions`
2. Um usuário só vê as próprias transcrições - nunca as de outro usuário
   (mesmo sabendo o `id` de uma transcrição alheia)
3. A resposta de `register` e `login` nunca contém o hash da senha
4. Um upload que não seja áudio (ex: `.pdf`) é recusado com 400, antes de
   chamar a Groq
5. A chave da Groq só existe no backend (`.env`), nunca é enviada ao
   frontend em nenhuma resposta

## 6. Fora de escopo (explicitamente)

- Edição ou exclusão de transcrições
- Recuperação de senha
- Papel de administrador
- Paginação do histórico (lista simples, sem limite nesta entrega)

## 7. Regras de senha

No cadastro, a senha deve ter no mínimo 8 caracteres, uma letra maiúscula, uma letra minúscula, um número e um caractere especial (qualquer símbolo que não seja letra nem número). A tela de cadastro mostra a lista de requisitos e marca cada um em verde quando é atendido. O backend impõe as mesmas regras e responde 400 se alguma falhar. O login não revalida essas regras.

## 8. Plano de etapas

Cada etapa foi pedida ao agente separadamente, verificada no terminal e registrada em um commit antes da seguinte.

### Etapa 1A: base do backend e módulo users
- Conexão com o PostgreSQL pelas variáveis `DB_*`, prefixo global `/api` e `ValidationPipe` global com `whitelist` e `forbidNonWhitelisted`.
- Entity `User` e `UsersService` (create, findByEmail e findById), sem rotas.
- Critérios de aceite:
  1. `npm --prefix backend run build` termina sem erros.
  2. O servidor sobe e a tabela `users` é criada com `id` uuid, `email` único, `passwordHash` e `createdAt`.

### Etapa 1B: autenticação
- `POST /api/auth/register` e `POST /api/auth/login`, JWT assinado com `JWT_SECRET`, senha com hash bcrypt e `JwtAuthGuard` global, com `@Public()` nas duas rotas abertas.
- Critérios de aceite:
  1. Cadastro válido responde 201 com `{ user: { id, name, email }, accessToken }`, sem `passwordHash`.
  2. E-mail repetido responde 409.
  3. Cadastro com campo `role` responde 400.
  4. Login correto responde 200, e senha errada ou e-mail inexistente respondem 401 com a mesma mensagem.
  5. No banco, a senha começa com `$2b$`.

### Etapa 2: transcrições
- `GET /api/transcriptions` e `POST /api/transcriptions` (multipart, campo `file`), chamada à Groq feita só pelo backend e histórico filtrado pelo usuário do token.
- Critérios de aceite:
  1. Sem token, as duas rotas respondem 401.
  2. Um áudio válido responde 201 com `id`, `text`, `originalFilename` e `createdAt`.
  3. Um arquivo que não é áudio responde 400, antes de chamar a Groq.
  4. A listagem devolve apenas as transcrições do usuário autenticado, da mais recente para a mais antiga.
  5. Falha na Groq responde 502, e a chave nunca aparece em resposta nenhuma.

### Etapa 3: frontend
- Tela única de login e cadastro, área interna protegida com envio de áudio e histórico. Todas as chamadas usam o caminho relativo `/api`, pelo proxy do Vite.
- Critérios de aceite:
  1. `/app` sem sessão redireciona para `/`, e `/` com sessão redireciona para `/app`.
  2. Cadastro, login e saída funcionam pela tela.
  3. Enviar o áudio de teste mostra o texto no topo do histórico.

### Etapa 4: ajustes finais
- Regras de senha validadas na tela e no backend (seção 7), botão para mostrar a senha e coluna `createdAt` com fuso horário (`timestamptz`).
- Critérios de aceite:
  1. Os cinco requisitos da senha ficam verdes um a um na aba "Criar conta".
  2. Senha sem caractere especial no cadastro responde 400 pela API.
  3. O horário do histórico bate com o relógio do computador.

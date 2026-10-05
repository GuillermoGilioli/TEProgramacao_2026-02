# Projeto — Ditado (transcrição de áudio)

Especificação completa em docs/ESPECIFICACAO.md. Leia antes de qualquer tarefa.

## Stack
- Frontend: React + Vite + TypeScript, react-router-dom e axios. Estado local com useState e CSS próprio (sem Tailwind, TanStack Query, Zustand nem react-hook-form)
- Backend: NestJS 12 (CommonJS) + TypeORM 1.x + PostgreSQL, @nestjs/jwt + @nestjs/passport + passport-jwt, bcryptjs, class-validator
- Banco: PostgreSQL 17, via docker-compose.yml (porta 5432, só 127.0.0.1)
- Transcrição: Groq (Whisper), modelo whisper-large-v3-turbo, chamada com fetch e FormData nativos do Node (sem groq-sdk)

## Ambiente
- Sistema: Windows, terminal PowerShell
- PowerShell não aceita && entre comandos e não tem grep. Rode um comando por vez
- Comandos partem da raiz do projeto, com npm --prefix backend ou npm --prefix frontend
- O backend foi criado com o scaffolding oficial (nest new). Não recrie package.json, tsconfig.json nem nest-cli.json
- Não altere versões de pacotes. TypeScript fica na série 6 (a 7 quebra o Nest CLI)

## Portas
- Frontend (Vite): 5173
- Backend (NestJS): 3000
- Banco (Postgres): 5432
- O frontend chama a API sempre por caminho relativo /api (proxy do Vite), nunca por http://localhost:3000

## Variáveis de ambiente (backend/.env)
- GROQ_API_KEY, GROQ_MODEL, JWT_SECRET, JWT_EXPIRES_IN
- DB_HOST=localhost, DB_PORT=5432, DB_USER=ditado, DB_PASSWORD=ditado, DB_NAME=ditado
- O backend roda na máquina, fora do Docker. DB_HOST nunca é "db"
- Nunca ler, mostrar nem commitar o .env. Só o .env.example, sem valores reais
- Ler variáveis com ConfigService.getOrThrow, nunca com process.env

## Convenções do backend
- main.ts: setGlobalPrefix('api') e ValidationPipe nativo global com whitelist: true e forbidNonWhitelisted: true. Não criar pipe de validação customizado
- Propriedades de DTO e de entity usam asserção definitiva (email!: string). Nunca inicializar com valor falso (= '' ou = new Date())
- Controller não importa Repository do TypeORM nem tem regra de negócio. Isso é do Service
- JwtAuthGuard registrado como APP_GUARD global. Rotas abertas usam @Public() (register e login)
- O usuário autenticado chega por @CurrentUser('id'). O decorator devolve o campo pedido, e não o objeto inteiro
- Resposta de usuário nunca inclui passwordHash. Retornar só { id, name, email }
- Cadastro nunca aceita role. O whitelist recusa campos não declarados
- Senha do cadastro: 8 caracteres, maiúscula, minúscula, número e caractere especial. O login não revalida
- E-mail já cadastrado responde 409 (ConflictException). Credenciais inválidas respondem 401 com a mesma mensagem
- Transcrição só é lida ou criada pelo dono. Usar o userId do token, nunca um id vindo do corpo
- Falha na Groq vira BadGatewayException (502) e o motivo vai para o log com Logger
- Colunas de data usam timestamptz

## Comandos
- Subir o banco (na raiz): docker compose up -d
- Backend em dev: npm --prefix backend run start:dev
- Frontend em dev: npm --prefix frontend run dev
- Verificar compilação: npm --prefix backend run build

## Sempre
- Trabalhar só no escopo da etapa pedida. Não criar arquivos fora dela
- Ao terminar, rodar o build e mostrar a saída real. Não afirmar que passou sem mostrar
- Ao terminar cada etapa, rodar os critérios de aceite da especificação e mostrar a saída

## Nunca
- Nunca devolver passwordHash em nenhuma resposta
- Nunca aceitar role vindo do corpo do cadastro
- Nunca usar endereço absoluto (localhost:3000) no código do frontend
- Nunca usar try/catch que esconda o erro sem registrá-lo no log
- Nunca criar rotas fora da especificação
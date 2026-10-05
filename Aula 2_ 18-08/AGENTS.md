# AGENTS.md

## Comandos

- O Python fica atrás do launcher `py`; `python`/`pip` NÃO estão no PATH. Use `py -m ...` (ex.: `py -m pytest -q`, `py -m pip install pytest`).
- Verificar: `py -m pytest -q` (25 testes). Sem lint/typecheck configurado.
- Rodar a aplicação: `py -m notas`. Lê/grava `notas.csv` no diretório atual.

## Arquitetura

- Uma responsabilidade por módulo em `notas/`: `aluno` (modelo + validação), `avaliacoes` (média ponderada, pesos 3/3/4), `classificacao` (>=7 aprovado, >=5 exame, <5 reprovado), `persistencia` (I/O do CSV), `servico` (orquestração via `ServicoNotas`), `menu` (CLI), `__main__` (ponto de entrada). As regras puras (`avaliacoes`, `classificacao`, `aluno`) ficam livres de I/O para continuarem testáveis isoladamente.
- O CSV guarda apenas as notas brutas (`matricula,nome,nota1,nota2,nota3`); média e situação são recalculadas a cada listagem, nunca persistidas. Notas ausentes ficam como células vazias, carregadas como `None`.
- `ServicoNotas(arquivo)` aceita um caminho; os testes sempre usam arquivos em `tmp_path`, nunca o `notas.csv` padrão.

## Convenções

- Nomes de variáveis, funções e mensagens da CLI em português.
- Um módulo por responsabilidade — não misturar regra de negócio com I/O no mesmo arquivo.
- Toda função pública relevante deve ter teste correspondente em `tests/`.

## Nunca

- Não instalar dependência nova sem perguntar antes (o projeto é intencionalmente minimalista, usando só a biblioteca padrão).
- Não versionar `notas.csv` com dados reais de alunos.
- Não "corrigir" o mojibake de acentos no terminal do Windows alterando o encoding do código — é só exibição (CP850 vs UTF-8); o CSV já é gravado corretamente em UTF-8.

## Detalhes técnicos

- `pyproject.toml` define `pythonpath = ["."]` — necessário para o `import notas` funcionar dentro de `tests/`.
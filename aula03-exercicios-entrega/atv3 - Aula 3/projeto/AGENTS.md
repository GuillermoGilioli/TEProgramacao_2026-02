# AGENTS.md

## Visão geral do projeto

Este é um pequeno projeto didático (exercício de aula) contendo um conversor de
temperatura de linha de comando escrito em Python puro (apenas biblioteca padrão),
com uma suíte de testes pytest e dois documentos de processo (plano e
auto-revisão) descrevendo como o exercício foi feito.

## Estrutura de arquivos

- `converte.py` — script principal / CLI de conversão de temperatura (Celsius,
  Fahrenheit, Kelvin, nos dois sentidos).
- `test_converte.py` — testes pytest para `converte.py` (testes via subprocess
  chamando a CLI + testes diretos das funções internas).
- `PLANO_ETAPA1.md` — documento de planejamento descrevendo o estado do código
  antes da tarefa, o gap encontrado (`inf`/`nan` não tratados) e as decisões
  tomadas.
- `AUTOCORRECAO.md` — documento de auto-revisão contra os critérios de aceite,
  com os comandos rodados manualmente e os problemas encontrados e corrigidos
  (import não usado, comentário confuso).
- `__pycache__/` — bytecode compilado do Python (gerado automaticamente).
- `.pytest_cache/` — cache do pytest (gerado automaticamente).

## Como rodar o programa

```
python converte.py <valor> <unidade_origem> <unidade_destino>
```

Exemplo:

```
python converte.py 100 C F
212.0
```

Unidades válidas: `C` (Celsius), `F` (Fahrenheit), `K` (Kelvin). Aceitam
minúsculas e espaços ao redor (são normalizadas internamente).

Código de saída: `0` em sucesso, `1` em qualquer erro de validação ou uso
incorreto (mensagens de erro vão para stderr).

## Como rodar os testes

```
pytest -v
```

ou, especificamente:

```
pytest test_converte.py -v
```

A única dependência externa é `pytest` (não há `requirements.txt`,
`pyproject.toml` ou `pytest.ini` no projeto — instale com `pip install pytest`,
usando `--break-system-packages` ou um venv se o ambiente Python for
gerenciado externamente).

## Detalhes de implementação relevantes (`converte.py`)

- Constantes: `ZERO_ABSOLUTO_C = -273.15`, `TOLERANCIA = 1e-9` (para evitar que
  ruído de ponto flutuante rejeite indevidamente um valor no limite),
  `UNIDADES_VALIDAS = ("C", "F", "K")`, `NOMES_UNIDADES` (mapa sigla → nome por
  extenso).
- `EntradaInvalida` — exceção própria para erros de validação de entrada (com
  mensagem amigável ao usuário), separada de bugs/erros inesperados.
- `normalizar_unidade(unidade)` — normaliza (strip + upper) e valida a unidade;
  lança `EntradaInvalida` se não for C/F/K.
- `converter_para_celsius` / `converter_de_celsius` — conversões auxiliares
  passando sempre por Celsius como unidade intermediária.
- `converter_temperatura(valor, unidade_origem, unidade_destino)` — função
  principal de conversão; rejeita resultado abaixo do zero absoluto; arredonda
  o resultado para 10 casas decimais para eliminar ruído de ponto flutuante.
- `parsear_valor(texto)` — converte texto para `float`; rejeita valores não
  numéricos e também `inf`/`-inf`/`nan` (via `math.isfinite`), que são aceitos
  por `float()` mas não representam temperaturas reais.
- `main(argv)` — ponto de entrada da CLI: valida número de argumentos (deve
  ser exatamente 3), captura `EntradaInvalida` e imprime erro + uso em stderr
  retornando código 1.

## Validações de entrada cobertas

1. Unidade desconhecida (fora de C/F/K) — mensagem lista as unidades válidas.
2. Valor não numérico (ex.: `"abc"`) — mensagem própria.
3. Valor não finito (`inf`, `-inf`, `nan`) — rejeitado explicitamente (era o
   gap identificado em `PLANO_ETAPA1.md` e corrigido nesta tarefa).
4. Temperatura resultante abaixo do zero absoluto (-273.15 °C, com tolerância
   de ponto flutuante) — mensagem própria.
5. Número incorreto de argumentos na CLI — imprime uso e retorna código 1.

## Convenções observadas no código

- Comentários e docstrings em português, nomes de funções/variáveis também em
  português (`converter_temperatura`, `unidade_origem`, `valor_celsius`, etc.).
- Uso de type hints não é praticado no código (funções sem anotação de tipos).
- Sem uso de `argparse` — argumentos de linha de comando são lidos
  posicionalmente via `sys.argv`.
- Sem dependências externas em `converte.py` (só `math` e `sys` da stdlib).
- Testes organizados em pytest puro (sem classes), com nomes de teste
  descritivos em português (`test_aceite_...`, `test_conversoes_basicas_via_cli`,
  etc.) e uso de `@pytest.mark.parametrize` para casos repetitivos.

## Notas / observações

- Não há `.gitignore` observado no diretório do projeto além do gerado
  automaticamente dentro de `.pytest_cache/`; `__pycache__/` e
  `.pytest_cache/` estão presentes no diretório e provavelmente não deveriam
  ser versionados.
- `PLANO_ETAPA1.md` e `AUTOCORRECAO.md` são documentos de processo (registro de
  como a tarefa foi feita), não documentação de uso do projeto em si — podem
  ser úteis como contexto histórico, mas não substituem este arquivo.

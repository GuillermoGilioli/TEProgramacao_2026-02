# Decisões tomadas por conta própria

O pedido original foi apenas "crie um conversor de temperatura", sem nenhum detalhe adicional. Todas as decisões abaixo foram feitas sem input do usuário:

- **Linguagem**: escolhi Python 3, por ser simples de rodar em qualquer ambiente sem dependências externas.
- **Unidades suportadas**: Celsius (C), Fahrenheit (F) e Kelvin (K) — as três escalas de temperatura mais comuns. Não incluí escalas menos usuais (Rankine, Réaumur, etc).
- **Interface**: implementei duas formas de uso no mesmo script:
  - **Modo CLI (argumentos de linha de comando)**: `python conversor_temperatura.py <valor> <origem> <destino>`, ex: `python conversor_temperatura.py 100 C F`.
  - **Modo interativo**: se o script for executado sem argumentos, ele entra em um loop perguntando valor, unidade de origem e unidade de destino, permitindo múltiplas conversões até o usuário digitar "sair".
- **Formato de entrada**: o valor numérico aceita tanto ponto quanto vírgula como separador decimal (ex: `25.5` ou `25,5`).
- **Unidades de entrada/saída**: aceitas em maiúsculas ou minúsculas (ex: "c", "C", "f", "F" funcionam igual).
- **Formato de saída**: imprime no terminal uma linha no formato `<valor> <origem> = <resultado> <destino>` (ex: `100 C = 212 F`). O resultado é arredondado para até 2 casas decimais, sem zeros/decimais desnecessários (ex: `0 C = 273.15 K`, `32 F = 0 C`).
- **Tratamento de entrada inválida**:
  - Valor não numérico: mensagem de erro específica e o programa encerra com código de saída 1 (no modo CLI) ou pede novamente o valor (no modo interativo).
  - Unidade inválida (fora de C/F/K): mensagem de erro listando as unidades válidas.
  - Validação física: valores de Kelvin abaixo de zero (zero absoluto) são rejeitados como inválidos, tanto na entrada quanto se o resultado da conversão desse um Kelvin negativo.
  - Número incorreto de argumentos no modo CLI: mostra uma mensagem de uso (`Uso: ...`) com exemplo, em vez de travar com um erro genérico do Python.
- **Código de saída**: no modo CLI, o script retorna exit code 1 em qualquer situação de erro (para permitir uso em scripts/automação) e 0 em caso de sucesso.
- **Idioma**: mensagens de uso, erros e prompts foram escritos em português, já que o pedido foi feito em português.
- **Não criei testes automatizados nem arquivo de dependências (requirements.txt)**, pois o script não usa nenhuma biblioteca externa (apenas a stdlib do Python).
- **Estrutura do código**: separei funções puras de conversão (célsius↔fahrenheit, célsius↔kelvin, fahrenheit↔kelvin) de funções de interface (CLI e interativa), para deixar a lógica de conversão testável/reutilizável isoladamente, embora nenhum teste tenha sido pedido nem escrito.
- **Nome do arquivo**: `conversor_temperatura.py`, escolhido por ser descritivo em português, consistente com o pedido original.

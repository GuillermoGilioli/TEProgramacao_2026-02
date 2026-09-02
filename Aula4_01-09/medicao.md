# Medição — economia de contexto com subagente

## Rodada A — sem subagente

Pergunta: "Investigue o pacote mcp instalado em .venv e me diga, em um parágrafo,
quais transportes ele suporta e em quais arquivos cada um está implementado."

Chamadas na sessão principal: 11
- 5x Get-ChildItem (listagens de diretório)
- 2x Grep (busca por "transport")
- 4x Read (__init__.py, stdio.py, sse.py, streamable_http.py)

## Rodada B — com subagente (@explore)

Mesma pergunta, delegada ao subagente @explore.

Chamadas na sessão principal: 0
Toda a investigação (as mesmas ~11 leituras) aconteceu na janela do subagente.
A sessão principal recebeu apenas o parágrafo de conclusão.

## Conclusão

O subagente não reduziu o número de leituras necessárias (a investigação
continuou levando o mesmo volume de trabalho), mas moveu esse custo para
uma janela separada. A resposta final foi equivalente nas duas rodadas,
mas na Rodada B a sessão principal ficou livre para seguir a conversa sem
carregar o conteúdo de nenhum dos arquivos do pacote mcp.

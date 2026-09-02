# Relato da atividade

**O que foi pedido**
Implementar um servidor MCP (diário) para lançamento e consulta de notas de alunos, com cálculo de média ponderada (pesos 3, 3, 4) e situação (aprovado/exame/reprovado/incompleto). A atividade inclui as quatro ferramentas MCP (listar_alunos, boletim, lancar_nota, resumo_turma) e o recurso diario://regras, além de uma Skill de relatório e um subagente auditor.

**O que foi feito**
O servidor `servidor.py` foi criado com as quatro ferramentas MCP e um recurso de regras, testado primeiro isoladamente no MCP Inspector e depois conectado ao OpenCode via `opencode.json`. Foi criada a Skill `relatorio-de-atividade`, acionada corretamente pela descrição sem citar o nome dela. Foi criado o subagente `auditor-de-contexto`, com permissões restritas (edit/bash/webfetch negados), que auditou o `AGENTS.md` gerado pelo `/init` e apontou a falta de uma descrição de propósito no topo do arquivo, corrigida em seguida. Foi feita a medição de economia de contexto (seção `medicao.md`): 11 chamadas de leitura na sessão principal sem subagente, contra 0 chamadas quando a mesma investigação foi delegada ao `@explore`.

**O que falhou**
Observação: o CSV inicial foi gravado com BOM, causando erro (`KeyError: 'matricula'`) na ferramenta `lancar_nota`.

**Como foi resolvido**
Recriado o arquivo sem BOM, usando `UTF8Encoding($false)`.

**Ferramentas de IA**
Agente OpenCode com modelo nemotron-3.5-lightning-free: implementou o servidor MCP, a Skill, o subagente e o AGENTS.md; identificou o erro de BOM; gerou o relatório técnico. Claude (Anthropic) auxiliou na condução do laboratório, diagnóstico do erro via leitura do traceback, orientação dos comandos PowerShell e revisão deste relatório.

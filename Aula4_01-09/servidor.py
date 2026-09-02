"""Servidor MCP do diário da disciplina."""

import csv
from pathlib import Path

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

ARQUIVO = Path(__file__).parent / "dados" / "turma.csv"
COLUNAS = ["matricula", "nome", "n1", "n2", "n3"]
PESOS = (3, 3, 4)

mcp = MCPServer("diario")

def _ler():
    with ARQUIVO.open(encoding="utf-8", newline="") as arq:
        return list(csv.DictReader(arq))

def _gravar(linhas):
    with ARQUIVO.open("w", encoding="utf-8", newline="") as arq:
        escritor = csv.DictWriter(arq, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(linhas)

def _media(linha):
    notas = [linha["n1"], linha["n2"], linha["n3"]]
    if any(nota.strip() == "" for nota in notas):
        return None
    soma = sum(float(nota) * peso for nota, peso in zip(notas, PESOS))
    return round(soma / sum(PESOS), 2)

def _situacao(media):
    if media is None:
        return "incompleto"
    if media >= 7.0:
        return "aprovado"
    if media >= 5.0:
        return "exame"
    return "reprovado"

def _buscar(linhas, matricula):
    for linha in linhas:
        if linha["matricula"] == matricula:
            return linha
    raise ToolError(f"matricula {matricula} nao existe na turma")

@mcp.tool()
def listar_alunos() -> str:
    """Lista a turma inteira com matrícula, nome, notas lançadas e situação atual."""
    saida = ["matricula   nome                  n1    n2    n3    media  situacao"]
    for linha in _ler():
        media = _media(linha)
        saida.append(
            f"{linha['matricula']:<10} {linha['nome']:<20} "
            f"{linha['n1'] or '-':<5} {linha['n2'] or '-':<5} {linha['n3'] or '-':<5} "
            f"{media if media is not None else '-':<6} {_situacao(media)}"
        )
    return "\n".join(saida)

@mcp.tool()
def boletim(matricula: str) -> str:
    """Boletim de um aluno: as três notas, a média ponderada e a situação."""
    linha = _buscar(_ler(), matricula)
    media = _media(linha)
    return (
        f"{linha['nome']} ({linha['matricula']})\n"
        f"  N1 (peso 3): {linha['n1'] or 'nao lancada'}\n"
        f"  N2 (peso 3): {linha['n2'] or 'nao lancada'}\n"
        f"  N3 (peso 4): {linha['n3'] or 'nao lancada'}\n"
        f"  media: {media if media is not None else 'incompleta'}\n"
        f"  situacao: {_situacao(media)}"
    )

@mcp.tool()
def lancar_nota(matricula: str, avaliacao: int, valor: float) -> str:
    """Lança a nota de uma avaliação (1, 2 ou 3) de um aluno, sobrescrevendo a anterior."""
    if avaliacao not in (1, 2, 3):
        raise ToolError("avaliacao deve ser 1, 2 ou 3")
    if not 0 <= valor <= 10:
        raise ToolError(f"nota invalida: {valor}. A nota deve estar entre 0 e 10.")
    linhas = _ler()
    linha = _buscar(linhas, matricula)
    anterior = linha[f"n{avaliacao}"] or "nao lancada"
    linha[f"n{avaliacao}"] = f"{valor:.1f}"
    _gravar(linhas)
    media = _media(linha)
    return (
        f"N{avaliacao} de {linha['nome']}: {anterior} -> {valor:.1f}. "
        f"Media agora: {media if media is not None else 'incompleta'} "
        f"({_situacao(media)})."
    )

@mcp.tool()
def resumo_turma() -> str:
    """Resumo da turma: contagem por situação, média geral e histograma das médias."""
    linhas = _ler()
    medias = [m for m in (_media(linha) for linha in linhas) if m is not None]
    contagem = {"aprovado": 0, "exame": 0, "reprovado": 0, "incompleto": 0}
    for linha in linhas:
        contagem[_situacao(_media(linha))] += 1

    faixas = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10.01)]
    histograma = []
    for inicio, fim in faixas:
        quantos = sum(1 for m in medias if inicio <= m < fim)
        histograma.append(f"  {inicio:>2}-{min(fim, 10):<2} | {'#' * quantos} {quantos}")

    geral = round(sum(medias) / len(medias), 2) if medias else "sem media"
    return (
        f"turma: {len(linhas)} alunos | media geral: {geral}\n"
        + " | ".join(f"{k}: {v}" for k, v in contagem.items())
        + "\n"
        + "\n".join(histograma)
    )

@mcp.resource("diario://regras")
def regras() -> str:
    """As regras de cálculo do diário: pesos das avaliações e limites de situação."""
    return (
        "Media ponderada com pesos N1=3, N2=3, N3=4.\n"
        "aprovado: media >= 7.0 | exame: media >= 5.0 | reprovado: media < 5.0\n"
        "Aluno com alguma avaliacao nao lancada fica como incompleto."
    )

if __name__ == "__main__":
    mcp.run()

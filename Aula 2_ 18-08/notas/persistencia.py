"""Leitura e escrita dos dados em arquivo CSV local.

Nenhum banco de dados é usado: os dados ficam em um arquivo CSV simples.
"""

import csv
from pathlib import Path

from .aluno import Aluno

CABECALHO = ["matricula", "nome", "nota1", "nota2", "nota3"]


def _converter_nota(valor):
    """Converte o texto do CSV em float; célula vazia vira None."""
    if valor == "":
        return None
    return float(valor)


def carregar(caminho):
    """Carrega os alunos do CSV.

    Devolve um dicionário no formato
    {matricula: (Aluno, (n1, n2, n3))}.
    Se o arquivo não existir, devolve um dicionário vazio.
    """
    arquivo = Path(caminho)
    alunos = {}
    if not arquivo.exists():
        return alunos
    with open(arquivo, "r", encoding="utf-8", newline="") as arquivo_aberto:
        for linha in csv.DictReader(arquivo_aberto):
            matricula = linha["matricula"]
            aluno = Aluno(matricula=matricula, nome=linha["nome"])
            notas = (
                _converter_nota(linha["nota1"]),
                _converter_nota(linha["nota2"]),
                _converter_nota(linha["nota3"]),
            )
            alunos[matricula] = (aluno, notas)
    return alunos


def salvar(caminho, alunos):
    """Grava todos os alunos (com suas notas) no CSV."""
    arquivo = Path(caminho)
    with open(arquivo, "w", encoding="utf-8", newline="") as arquivo_aberto:
        escritor = csv.DictWriter(arquivo_aberto, fieldnames=CABECALHO)
        escritor.writeheader()
        for aluno, notas in alunos.values():
            escritor.writerow(
                {
                    "matricula": aluno.matricula,
                    "nome": aluno.nome,
                    "nota1": notas[0] if notas[0] is not None else "",
                    "nota2": notas[1] if notas[1] is not None else "",
                    "nota3": notas[2] if notas[2] is not None else "",
                }
            )
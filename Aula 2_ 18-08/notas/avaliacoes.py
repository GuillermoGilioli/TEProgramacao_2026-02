"""Lançamento das avaliações e cálculo da média ponderada.

A disciplina possui 3 avaliações com pesos 3, 3 e 4.
"""

PESOS = (3, 3, 4)


def validar_nota(valor):
    """Converte o valor para float e garante que está entre 0 e 10."""
    try:
        nota = float(valor)
    except (TypeError, ValueError):
        raise ValueError("Nota inválida: informe um número.")
    if nota < 0 or nota > 10:
        raise ValueError("A nota deve estar entre 0 e 10.")
    return nota


def calcular_media(nota1, nota2, nota3):
    """Calcula a média ponderada das 3 avaliações (pesos 3, 3 e 4)."""
    notas = (validar_nota(nota1), validar_nota(nota2), validar_nota(nota3))
    soma_pesos = sum(PESOS)
    soma_ponderada = sum(nota * peso for nota, peso in zip(notas, PESOS))
    return round(soma_ponderada / soma_pesos, 2)
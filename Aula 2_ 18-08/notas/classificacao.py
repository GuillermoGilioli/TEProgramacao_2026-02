"""Classificação do aluno conforme a média final."""

APROVADO = "aprovado"
EXAME = "exame"
REPROVADO = "reprovado"


def classificar(media):
    """Retorna a situação do aluno conforme a média.

    Regras:
        média >= 7 -> aprovado
        média >= 5 -> exame
        média <  5 -> reprovado
    """
    if media >= 7:
        return APROVADO
    if media >= 5:
        return EXAME
    return REPROVADO
"""Normaliza nomes de alunos para exibição.

Regras aplicadas:
- Remove espaços extras nas bordas e entre palavras (múltiplos espaços viram um só).
- Cada palavra é capitalizada (primeira letra maiúscula, restante minúscula).
- Preposições comuns em nomes portugueses ("de", "da", "do", "das", "dos")
  permanecem em minúsculas, exceto se forem a primeira palavra do nome.
"""

# Preposições que devem permanecer em minúsculas (exceto na primeira posição).
PREPOSICOES_MINUSCULAS = {"de", "da", "do", "das", "dos"}


def normaliza_nome(nome: str) -> str:
    """Normaliza um nome de aluno para exibição.

    Args:
        nome: nome bruto, possivelmente com espaços extras e capitalização
            inconsistente (ex.: " ana  MARIA silva ").

    Returns:
        Nome normalizado, com espaços colapsados e capitalização padrão,
        mantendo preposições (de/da/do/das/dos) em minúsculas quando não
        forem a primeira palavra.
    """
    palavras = nome.split()

    resultado = []
    for indice, palavra in enumerate(palavras):
        palavra_lower = palavra.lower()
        if indice > 0 and palavra_lower in PREPOSICOES_MINUSCULAS:
            resultado.append(palavra_lower)
        else:
            resultado.append(palavra_lower.capitalize())

    return " ".join(resultado)


if __name__ == "__main__":
    exemplos = [
        " ana  MARIA silva ",
        "JOSE DOS SANTOS",
        "maria  da  CONCEICAO",
    ]
    for exemplo in exemplos:
        print(repr(exemplo), "->", repr(normaliza_nome(exemplo)))

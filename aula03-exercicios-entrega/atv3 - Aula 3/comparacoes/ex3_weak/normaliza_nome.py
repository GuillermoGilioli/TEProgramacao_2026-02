"""Normaliza nomes de alunos para exibicao.

Regra de normalizacao adotada:
- Remove espacos extras no inicio/fim e colapsa espacos internos multiplos em um so.
- Cada palavra fica com a primeira letra maiuscula e o restante minusculo
  (ex.: "MARIA" -> "Maria", "conceicao" -> "Conceicao"), preservando acentuacao.
- Um conjunto de preposicoes/conectivos comuns em nomes portugueses
  (de, da, do, das, dos, e) fica em minusculas, exceto quando e a primeira
  palavra do nome.
"""

# Palavras que, por convencao, ficam em minusculas quando nao sao a primeira
# palavra do nome (preposicoes e conectivos comuns em nomes em portugues).
PALAVRAS_MINUSCULAS = {"de", "da", "do", "das", "dos", "e"}


def normaliza_nome(nome: str) -> str:
    """Normaliza um nome de aluno para exibicao.

    Args:
        nome: nome bruto do aluno, em qualquer combinacao de maiusculas/
            minusculas e com possiveis espacos extras.

    Returns:
        Nome normalizado, com cada palavra capitalizada e preposicoes
        comuns (de, da, do, das, dos, e) em minusculas, exceto quando
        forem a primeira palavra.

    Raises:
        ValueError: se o nome estiver vazio ou contiver apenas espacos.
    """
    if not isinstance(nome, str):
        raise TypeError("nome deve ser uma string")

    palavras = nome.split()

    if not palavras:
        raise ValueError("nome nao pode ser vazio")

    nome_normalizado = []
    for indice, palavra in enumerate(palavras):
        palavra_lower = palavra.lower()
        if indice > 0 and palavra_lower in PALAVRAS_MINUSCULAS:
            nome_normalizado.append(palavra_lower)
        else:
            nome_normalizado.append(palavra.capitalize())

    return " ".join(nome_normalizado)


if __name__ == "__main__":
    exemplos = [
        "maria da CONCEICAO",
        "PEDRO DE ALCANTARA e SILVA",
    ]
    for exemplo in exemplos:
        print(f"{exemplo!r} -> {normaliza_nome(exemplo)!r}")

def media_ponderada(notas, pesos):
    """Calcula a média ponderada de uma lista de notas com seus respectivos pesos.

    Args:
        notas: lista de notas.
        pesos: lista de pesos correspondentes a cada nota.

    Returns:
        float: a média ponderada das notas.

    Raises:
        ValueError: se as listas tiverem tamanhos diferentes.
        ValueError: se a soma dos pesos for igual a zero.
    """
    if len(notas) != len(pesos):
        raise ValueError("As listas 'notas' e 'pesos' devem ter o mesmo tamanho.")

    soma_pesos = sum(pesos)
    if soma_pesos == 0:
        raise ValueError("A soma dos pesos não pode ser igual a zero.")

    soma_ponderada = sum(nota * peso for nota, peso in zip(notas, pesos))
    return soma_ponderada / soma_pesos


if __name__ == "__main__":
    print(media_ponderada([8, 7, 9], [3, 3, 4]))

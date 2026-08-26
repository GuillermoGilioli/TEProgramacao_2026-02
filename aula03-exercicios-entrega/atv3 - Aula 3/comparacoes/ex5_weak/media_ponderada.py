def media_ponderada(valores, pesos):
    """
    Calcula a média ponderada de uma lista de valores com seus respectivos pesos.

    Args:
        valores (list[float]): lista de valores numéricos.
        pesos (list[float]): lista de pesos correspondentes a cada valor.

    Returns:
        float: a média ponderada dos valores.

    Raises:
        ValueError: se as listas tiverem tamanhos diferentes, estiverem vazias
            ou se a soma dos pesos for zero.
    """
    if len(valores) != len(pesos):
        raise ValueError("As listas 'valores' e 'pesos' devem ter o mesmo tamanho.")

    if len(valores) == 0:
        raise ValueError("As listas não podem estar vazias.")

    soma_pesos = sum(pesos)
    if soma_pesos == 0:
        raise ValueError("A soma dos pesos não pode ser zero.")

    soma_ponderada = sum(v * p for v, p in zip(valores, pesos))

    return soma_ponderada / soma_pesos


if __name__ == "__main__":
    notas = [7.0, 8.5, 6.0]
    pesos = [2, 3, 5]

    resultado = media_ponderada(notas, pesos)
    print(f"Média ponderada: {resultado:.2f}")

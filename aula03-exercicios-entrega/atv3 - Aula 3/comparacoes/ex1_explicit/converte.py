#!/usr/bin/env python3
"""Conversor de temperatura por linha de comando.

Converte entre Celsius (C), Fahrenheit (F) e Kelvin (K), nos dois sentidos.

Uso:
    python converte.py <valor> <unidade_origem> <unidade_destino>

Exemplo:
    python converte.py 100 C F
    212.0

Este script usa apenas a biblioteca padrão do Python. O foco principal é a
validação de entrada (unidade desconhecida, valor não numérico, temperatura
abaixo do zero absoluto), já que o cálculo de conversão em si é trivial.
"""

import sys

# Zero absoluto em Celsius. Nenhuma temperatura real pode ser menor que isso.
ZERO_ABSOLUTO_C = -273.15

# Tolerância para erros de arredondamento de ponto flutuante ao comparar
# com o zero absoluto (ex.: um valor calculado como -273.15000000000003
# não deve ser recusado por causa de imprecisão numérica).
TOLERANCIA = 1e-9

UNIDADES_VALIDAS = ("C", "F", "K")

NOMES_UNIDADES = {
    "C": "Celsius",
    "F": "Fahrenheit",
    "K": "Kelvin",
}


class EntradaInvalida(Exception):
    """Erro de validação da entrada do usuário, com mensagem amigável."""


def formatar_unidades_validas():
    itens = [f"{sigla} ({NOMES_UNIDADES[sigla]})" for sigla in UNIDADES_VALIDAS]
    return ", ".join(itens)


def normalizar_unidade(unidade):
    """Valida e normaliza uma unidade (aceita minúscula ou maiúscula)."""
    unidade_normalizada = unidade.strip().upper()
    if unidade_normalizada not in UNIDADES_VALIDAS:
        raise EntradaInvalida(
            f"Unidade desconhecida: '{unidade}'. "
            f"Unidades válidas: {formatar_unidades_validas()}."
        )
    return unidade_normalizada


def converter_para_celsius(valor, unidade_origem):
    """Converte um valor de uma unidade qualquer para Celsius."""
    if unidade_origem == "C":
        return valor
    if unidade_origem == "F":
        return (valor - 32) * 5 / 9
    if unidade_origem == "K":
        return valor - 273.15
    raise AssertionError(f"unidade não tratada: {unidade_origem}")


def converter_de_celsius(valor_celsius, unidade_destino):
    """Converte um valor em Celsius para a unidade de destino."""
    if unidade_destino == "C":
        return valor_celsius
    if unidade_destino == "F":
        return valor_celsius * 9 / 5 + 32
    if unidade_destino == "K":
        return valor_celsius + 273.15
    raise AssertionError(f"unidade não tratada: {unidade_destino}")


def converter_temperatura(valor, unidade_origem, unidade_destino):
    """Converte `valor` de `unidade_origem` para `unidade_destino`.

    Lança EntradaInvalida se a temperatura resultante for fisicamente
    impossível (abaixo do zero absoluto).
    """
    origem = normalizar_unidade(unidade_origem)
    destino = normalizar_unidade(unidade_destino)

    valor_celsius = converter_para_celsius(valor, origem)

    if valor_celsius < ZERO_ABSOLUTO_C - TOLERANCIA:
        raise EntradaInvalida(
            f"Temperatura inválida: {valor} {origem} está abaixo do zero "
            f"absoluto ({ZERO_ABSOLUTO_C} °C). Nenhuma temperatura real pode "
            "ser menor que isso."
        )

    resultado = converter_de_celsius(valor_celsius, destino)

    # Arredonda para eliminar ruído de ponto flutuante (ex.: 98.60000000000001),
    # sem afetar a precisão relevante para o uso didático do script.
    return round(resultado, 10)


def parsear_valor(texto):
    """Converte o texto do valor de entrada em float, com mensagem própria."""
    try:
        return float(texto)
    except ValueError:
        raise EntradaInvalida(
            f"Valor inválido: '{texto}'. Informe um número, "
            "por exemplo: 100 ou -40.5."
        )


def uso():
    return (
        "Uso: python converte.py <valor> <unidade_origem> <unidade_destino>\n"
        f"Unidades válidas: {formatar_unidades_validas()}.\n"
        "Exemplo: python converte.py 100 C F"
    )


def main(argv):
    if len(argv) != 3:
        print("Erro: número incorreto de argumentos.", file=sys.stderr)
        print(uso(), file=sys.stderr)
        return 1

    valor_texto, unidade_origem, unidade_destino = argv

    try:
        valor = parsear_valor(valor_texto)
        resultado = converter_temperatura(valor, unidade_origem, unidade_destino)
    except EntradaInvalida as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    print(resultado)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

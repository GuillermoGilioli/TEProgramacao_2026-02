#!/usr/bin/env python3
"""
Conversor de Temperatura

Converte valores de temperatura entre Celsius (C), Fahrenheit (F) e Kelvin (K).

Uso via linha de comando:
    python conversor_temperatura.py 100 C F
    python conversor_temperatura.py 32 F C
    python conversor_temperatura.py 0 C K

Uso interativo (sem argumentos):
    python conversor_temperatura.py
"""

import sys

UNIDADES_VALIDAS = ("C", "F", "K")


def celsius_para_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def fahrenheit_para_celsius(f: float) -> float:
    return (f - 32) * 5 / 9


def celsius_para_kelvin(c: float) -> float:
    return c + 273.15


def kelvin_para_celsius(k: float) -> float:
    return k - 273.15


def fahrenheit_para_kelvin(f: float) -> float:
    return celsius_para_kelvin(fahrenheit_para_celsius(f))


def kelvin_para_fahrenheit(k: float) -> float:
    return celsius_para_fahrenheit(kelvin_para_celsius(k))


def converter(valor: float, origem: str, destino: str) -> float:
    origem = origem.upper()
    destino = destino.upper()

    if origem not in UNIDADES_VALIDAS or destino not in UNIDADES_VALIDAS:
        raise ValueError(
            f"Unidade invalida. Use uma das seguintes: {', '.join(UNIDADES_VALIDAS)}."
        )

    if origem == "K" and valor < 0:
        raise ValueError("Temperatura em Kelvin nao pode ser negativa (abaixo do zero absoluto).")

    if origem == destino:
        return valor

    conversoes = {
        ("C", "F"): celsius_para_fahrenheit,
        ("F", "C"): fahrenheit_para_celsius,
        ("C", "K"): celsius_para_kelvin,
        ("K", "C"): kelvin_para_celsius,
        ("F", "K"): fahrenheit_para_kelvin,
        ("K", "F"): kelvin_para_fahrenheit,
    }

    resultado = conversoes[(origem, destino)](valor)

    if destino == "K" and resultado < 0:
        raise ValueError("Resultado em Kelvin seria negativo (abaixo do zero absoluto), entrada invalida.")

    return resultado


def formatar_resultado(valor: float) -> str:
    return f"{round(valor, 2):g}"


def modo_interativo():
    print("=== Conversor de Temperatura ===")
    print(f"Unidades suportadas: {', '.join(UNIDADES_VALIDAS)} (Celsius, Fahrenheit, Kelvin)")
    print("Digite 'sair' a qualquer momento para encerrar.\n")

    while True:
        entrada_valor = input("Valor a converter: ").strip()
        if entrada_valor.lower() in ("sair", "exit", "quit"):
            print("Encerrando o conversor.")
            break

        try:
            valor = float(entrada_valor.replace(",", "."))
        except ValueError:
            print("Erro: valor invalido. Digite um numero (ex: 25 ou 25.5).\n")
            continue

        origem = input(f"Unidade de origem ({'/'.join(UNIDADES_VALIDAS)}): ").strip()
        if origem.lower() in ("sair", "exit", "quit"):
            print("Encerrando o conversor.")
            break

        destino = input(f"Unidade de destino ({'/'.join(UNIDADES_VALIDAS)}): ").strip()
        if destino.lower() in ("sair", "exit", "quit"):
            print("Encerrando o conversor.")
            break

        try:
            resultado = converter(valor, origem, destino)
            print(f"Resultado: {formatar_resultado(valor)} {origem.upper()} = {formatar_resultado(resultado)} {destino.upper()}\n")
        except ValueError as erro:
            print(f"Erro: {erro}\n")


def modo_cli(argv):
    if len(argv) != 3:
        print("Uso: python conversor_temperatura.py <valor> <unidade_origem> <unidade_destino>")
        print("Exemplo: python conversor_temperatura.py 100 C F")
        print(f"Unidades validas: {', '.join(UNIDADES_VALIDAS)}")
        sys.exit(1)

    valor_str, origem, destino = argv

    try:
        valor = float(valor_str.replace(",", "."))
    except ValueError:
        print(f"Erro: '{valor_str}' nao e um numero valido.")
        sys.exit(1)

    try:
        resultado = converter(valor, origem, destino)
    except ValueError as erro:
        print(f"Erro: {erro}")
        sys.exit(1)

    print(f"{formatar_resultado(valor)} {origem.upper()} = {formatar_resultado(resultado)} {destino.upper()}")


def main():
    argv = sys.argv[1:]
    if not argv:
        modo_interativo()
    else:
        modo_cli(argv)


if __name__ == "__main__":
    main()

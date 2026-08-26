#!/usr/bin/env python3
"""
Le um arquivo CSV com as colunas: data,produto,valor
e imprime a soma da coluna 'valor'.

Usa apenas a biblioteca padrao do Python (modulo csv), pois o script
precisa rodar em um servidor sem acesso a internet para instalar pacotes.

Uso:
    python3 soma_valores.py caminho/para/arquivo.csv
"""

import csv
import sys


def parse_valor(valor_str):
    """Converte o texto da coluna 'valor' para float.

    Aceita tanto '10.50' (ponto decimal) quanto '10,50' (virgula decimal,
    comum em CSVs gerados no Brasil), pois o formato nao foi especificado
    no pedido original.
    """
    valor_str = valor_str.strip()
    if "," in valor_str and "." not in valor_str:
        valor_str = valor_str.replace(",", ".")
    return float(valor_str)


def somar_valores(caminho_csv):
    """Le o CSV e retorna a soma da coluna 'valor'.

    Linhas com valor ausente ou invalido sao ignoradas (e reportadas em
    stderr), para que uma unica linha problematica nao derrube o script
    inteiro rodando em produção.
    """
    total = 0.0
    linhas_lidas = 0
    linhas_ignoradas = 0

    with open(caminho_csv, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        if leitor.fieldnames is None or "valor" not in leitor.fieldnames:
            raise ValueError(
                "CSV nao contem a coluna 'valor' no cabecalho. "
                f"Colunas encontradas: {leitor.fieldnames}"
            )

        for numero_linha, linha in enumerate(leitor, start=2):
            valor_bruto = linha.get("valor")
            if valor_bruto is None or valor_bruto.strip() == "":
                print(
                    f"Aviso: linha {numero_linha} sem valor na coluna 'valor', ignorada.",
                    file=sys.stderr,
                )
                linhas_ignoradas += 1
                continue

            try:
                total += parse_valor(valor_bruto)
                linhas_lidas += 1
            except ValueError:
                print(
                    f"Aviso: linha {numero_linha} tem valor invalido "
                    f"({valor_bruto!r}), ignorada.",
                    file=sys.stderr,
                )
                linhas_ignoradas += 1

    return total, linhas_lidas, linhas_ignoradas


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 soma_valores.py caminho/para/arquivo.csv", file=sys.stderr)
        sys.exit(1)

    caminho_csv = sys.argv[1]

    try:
        total, linhas_lidas, linhas_ignoradas = somar_valores(caminho_csv)
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_csv}' nao encontrado.", file=sys.stderr)
        sys.exit(1)
    except ValueError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        sys.exit(1)

    print(f"Linhas somadas: {linhas_lidas}")
    if linhas_ignoradas:
        print(f"Linhas ignoradas: {linhas_ignoradas}")
    print(f"Soma da coluna 'valor': {total:.2f}")


if __name__ == "__main__":
    main()

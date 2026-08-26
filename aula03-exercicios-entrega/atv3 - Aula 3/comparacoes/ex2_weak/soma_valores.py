#!/usr/bin/env python3
"""
Soma a coluna 'valor' de um arquivo CSV com colunas: data,produto,valor.

Nao usa bibliotecas externas (apenas biblioteca padrao do Python).

Uso:
    python soma_valores.py caminho/para/arquivo.csv

Se nenhum caminho for informado, tenta usar "dados.csv" no mesmo
diretorio deste script.
"""

import os
import sys


def somar_valores(caminho_arquivo):
    total = 0.0
    linhas_processadas = 0
    linhas_ignoradas = 0

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        primeira_linha = True

        for numero_linha, linha in enumerate(arquivo, start=1):
            linha = linha.strip()

            if not linha:
                continue

            # A primeira linha nao vazia e tratada como cabecalho
            # (espera-se: data,produto,valor) e e descartada.
            if primeira_linha:
                primeira_linha = False
                if linha.lower().replace(" ", "") == "data,produto,valor":
                    continue

            campos = linha.split(",")

            if len(campos) != 3:
                print(
                    f"Aviso: linha {numero_linha} ignorada (esperado 3 colunas, "
                    f"encontrado {len(campos)}): {linha!r}",
                    file=sys.stderr,
                )
                linhas_ignoradas += 1
                continue

            _data, _produto, valor_str = campos
            valor_str = valor_str.strip()

            try:
                valor = float(valor_str)
            except ValueError:
                print(
                    f"Aviso: linha {numero_linha} ignorada (valor invalido: {valor_str!r})",
                    file=sys.stderr,
                )
                linhas_ignoradas += 1
                continue

            total += valor
            linhas_processadas += 1

    return total, linhas_processadas, linhas_ignoradas


def main():
    if len(sys.argv) > 1:
        caminho_arquivo = sys.argv[1]
    else:
        caminho_arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados.csv")

    if not os.path.isfile(caminho_arquivo):
        print(f"Erro: arquivo nao encontrado: {caminho_arquivo}", file=sys.stderr)
        sys.exit(1)

    total, linhas_processadas, linhas_ignoradas = somar_valores(caminho_arquivo)

    print(f"Arquivo: {caminho_arquivo}")
    print(f"Linhas somadas: {linhas_processadas}")
    if linhas_ignoradas:
        print(f"Linhas ignoradas: {linhas_ignoradas}")
    print(f"Soma total de 'valor': {total:.2f}")


if __name__ == "__main__":
    main()

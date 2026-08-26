"""Testes pytest para converte.py.

Duas camadas de teste:
- Testes de CLI via subprocess: reproduzem fielmente os critérios de aceite,
  que são descritos em termos de invocação de linha de comando
  ("python converte.py 100 C F" imprime 212.0).
- Testes diretos das funções internas: mais rápidos, cobrem casos de borda
  numéricos sem precisar de spawn de processo.
"""

import subprocess
import sys
from pathlib import Path

import pytest

CONVERTE_PY = Path(__file__).parent / "converte.py"

# pytest insere o diretório do arquivo de teste em sys.path automaticamente
# (não há pacote/__init__.py aqui), então este import funciona mesmo estando
# abaixo de outras atribuições no módulo.
import converte  # noqa: E402


def rodar_cli(*args):
    """Executa `python converte.py <args>` e retorna o CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(CONVERTE_PY), *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Critérios de aceite originais
# ---------------------------------------------------------------------------


def test_aceite_100_c_para_f_imprime_212():
    resultado = rodar_cli("100", "C", "F")
    assert resultado.returncode == 0
    assert resultado.stdout.strip() == "212.0"


def test_aceite_abaixo_do_zero_absoluto_e_recusado_com_mensagem_propria():
    resultado = rodar_cli("-300", "C", "F")
    assert resultado.returncode != 0
    assert resultado.stdout.strip() == ""
    assert "zero absoluto" in resultado.stderr.lower()


def test_aceite_unidade_desconhecida_lista_unidades_validas():
    resultado = rodar_cli("100", "X", "F")
    assert resultado.returncode != 0
    stderr_lower = resultado.stderr.lower()
    assert "unidade desconhecida" in stderr_lower or "unidade" in stderr_lower
    # As três unidades válidas devem aparecer listadas na mensagem de erro.
    assert "C (Celsius)" in resultado.stderr
    assert "F (Fahrenheit)" in resultado.stderr
    assert "K (Kelvin)" in resultado.stderr


# ---------------------------------------------------------------------------
# Casos extras de CLI (comportamento que já existia ou foi reforçado)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "valor, origem, destino, esperado",
    [
        ("0", "C", "F", "32.0"),
        ("32", "F", "C", "0.0"),
        ("0", "C", "K", "273.15"),
        ("273.15", "K", "C", "0.0"),
        ("-40", "C", "F", "-40.0"),
        ("100", "C", "C", "100.0"),
    ],
)
def test_conversoes_basicas_via_cli(valor, origem, destino, esperado):
    resultado = rodar_cli(valor, origem, destino)
    assert resultado.returncode == 0
    assert resultado.stdout.strip() == esperado


def test_unidade_aceita_minuscula():
    resultado = rodar_cli("100", "c", "f")
    assert resultado.returncode == 0
    assert resultado.stdout.strip() == "212.0"


def test_unidade_aceita_espacos_ao_redor():
    resultado = rodar_cli("100", " C ", " F ")
    assert resultado.returncode == 0
    assert resultado.stdout.strip() == "212.0"


def test_valor_nao_numerico_e_recusado():
    resultado = rodar_cli("abc", "C", "F")
    assert resultado.returncode != 0
    assert "valor inválido" in resultado.stderr.lower()


def test_numero_incorreto_de_argumentos_mostra_uso():
    resultado = rodar_cli("100", "C")
    assert resultado.returncode != 0
    assert "uso:" in resultado.stderr.lower()


def test_sem_argumentos_mostra_uso():
    resultado = rodar_cli()
    assert resultado.returncode != 0
    assert "uso:" in resultado.stderr.lower()


def test_temperatura_exatamente_no_zero_absoluto_e_aceita():
    # -273.15 C é o limite exato, não deve ser recusado (só o que é MENOR).
    resultado = rodar_cli("-273.15", "C", "K")
    assert resultado.returncode == 0
    assert resultado.stdout.strip() == "0.0"


@pytest.mark.parametrize("valor", ["inf", "-inf", "Infinity", "nan"])
def test_valores_nao_finitos_sao_recusados(valor):
    resultado = rodar_cli(valor, "C", "F")
    assert resultado.returncode != 0
    assert resultado.stdout.strip() == ""
    assert "inválido" in resultado.stderr.lower()


# ---------------------------------------------------------------------------
# Testes diretos das funções internas (casos de borda numéricos)
# ---------------------------------------------------------------------------


def test_converter_temperatura_100_c_para_f():
    assert converte.converter_temperatura(100, "C", "F") == 212.0


def test_converter_temperatura_abaixo_do_zero_absoluto_levanta_erro():
    with pytest.raises(converte.EntradaInvalida, match="zero absoluto"):
        converte.converter_temperatura(-274, "C", "F")


def test_converter_temperatura_unidade_desconhecida_levanta_erro():
    with pytest.raises(converte.EntradaInvalida, match="Unidade desconhecida"):
        converte.converter_temperatura(100, "X", "F")


def test_parsear_valor_numero_valido():
    assert converte.parsear_valor("100") == 100.0


def test_parsear_valor_invalido_levanta_erro():
    with pytest.raises(converte.EntradaInvalida, match="Valor inválido"):
        converte.parsear_valor("abc")


@pytest.mark.parametrize("texto", ["inf", "-inf", "nan"])
def test_parsear_valor_nao_finito_levanta_erro(texto):
    with pytest.raises(converte.EntradaInvalida, match="finito"):
        converte.parsear_valor(texto)


def test_normalizar_unidade_case_insensitive():
    assert converte.normalizar_unidade(" c ") == "C"


def test_normalizar_unidade_invalida_mensagem_lista_validas():
    with pytest.raises(converte.EntradaInvalida) as excinfo:
        converte.normalizar_unidade("X")
    mensagem = str(excinfo.value)
    assert "C (Celsius)" in mensagem
    assert "F (Fahrenheit)" in mensagem
    assert "K (Kelvin)" in mensagem

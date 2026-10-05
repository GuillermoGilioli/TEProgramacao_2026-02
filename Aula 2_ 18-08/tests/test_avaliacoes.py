import pytest

from notas.avaliacoes import calcular_media, validar_nota


def test_media_todas_dez():
    assert calcular_media(10, 10, 10) == 10.0


def test_media_todas_zero():
    assert calcular_media(0, 0, 0) == 0.0


def test_media_ponderada():
    assert calcular_media(10, 10, 5) == 8.0


def test_media_ponderada_com_exame():
    assert calcular_media(5, 5, 10) == 7.0


def test_nota_negativa_gera_erro():
    with pytest.raises(ValueError):
        validar_nota(-1)


def test_nota_acima_de_dez_gera_erro():
    with pytest.raises(ValueError):
        validar_nota(10.1)


def test_nota_nao_numerica_gera_erro():
    with pytest.raises(ValueError):
        validar_nota("abc")
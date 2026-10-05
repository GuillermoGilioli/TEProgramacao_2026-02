from notas.classificacao import APROVADO, EXAME, REPROVADO, classificar


def test_media_sete_aprovado():
    assert classificar(7.0) == APROVADO


def test_media_dez_aprovado():
    assert classificar(10.0) == APROVADO


def test_media_seis_meio_exame():
    assert classificar(6.5) == EXAME


def test_media_cinco_exame():
    assert classificar(5.0) == EXAME


def test_media_abaixo_de_cinco_reprovado():
    assert classificar(4.9) == REPROVADO
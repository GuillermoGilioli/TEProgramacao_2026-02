import pytest

from notas.aluno import Aluno


def test_cria_aluno_valido():
    aluno = Aluno(matricula="2024001", nome="Maria Silva")
    assert aluno.matricula == "2024001"
    assert aluno.nome == "Maria Silva"


def test_remove_espacos_das_bordas():
    aluno = Aluno(matricula=" 2024001 ", nome=" Maria Silva ")
    assert aluno.matricula == "2024001"
    assert aluno.nome == "Maria Silva"


def test_matricula_vazia_gera_erro():
    with pytest.raises(ValueError):
        Aluno(matricula="   ", nome="Maria Silva")


def test_nome_vazio_gera_erro():
    with pytest.raises(ValueError):
        Aluno(matricula="2024001", nome="   ")
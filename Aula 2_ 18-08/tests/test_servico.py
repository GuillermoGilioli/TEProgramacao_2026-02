import pytest

from notas.servico import ServicoNotas


def test_cadastrar_e_listar_sem_notas(tmp_path):
    servico = ServicoNotas(tmp_path / "notas.csv")
    servico.cadastrar_aluno("2024001", "Maria Silva")
    turma = servico.listar_turma()
    assert len(turma) == 1
    assert turma[0]["nome"] == "Maria Silva"
    assert turma[0]["media"] is None
    assert turma[0]["situacao"] == "sem notas"


def test_matricula_duplicada_gera_erro(tmp_path):
    servico = ServicoNotas(tmp_path / "notas.csv")
    servico.cadastrar_aluno("2024001", "Maria Silva")
    with pytest.raises(ValueError):
        servico.cadastrar_aluno("2024001", "Outra Pessoa")


def test_lancar_notas_e_listar(tmp_path):
    servico = ServicoNotas(tmp_path / "notas.csv")
    servico.cadastrar_aluno("2024001", "Maria Silva")
    servico.lancar_notas("2024001", 10, 10, 5)
    turma = servico.listar_turma()
    assert turma[0]["media"] == 8.0
    assert turma[0]["situacao"] == "aprovado"


def test_lancar_notas_para_aluno_inexistente_gera_erro(tmp_path):
    servico = ServicoNotas(tmp_path / "notas.csv")
    with pytest.raises(ValueError):
        servico.lancar_notas("9999", 10, 10, 10)


def test_dados_persistem_entre_instancias(tmp_path):
    arquivo = tmp_path / "notas.csv"
    servico = ServicoNotas(arquivo)
    servico.cadastrar_aluno("2024001", "Maria Silva")
    servico.lancar_notas("2024001", 7, 8, 9)

    novo_servico = ServicoNotas(arquivo)
    turma = novo_servico.listar_turma()
    assert len(turma) == 1
    assert turma[0]["media"] == 8.1
    assert turma[0]["situacao"] == "aprovado"
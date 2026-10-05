from notas.aluno import Aluno
from notas.persistencia import carregar, salvar


def test_carregar_arquivo_inexistente_devolve_vazio(tmp_path):
    assert carregar(tmp_path / "nao_existe.csv") == {}


def test_salvar_e_carregar(tmp_path):
    arquivo = tmp_path / "notas.csv"
    alunos = {
        "2024001": (Aluno("2024001", "Maria Silva"), (10, 10, 5)),
    }
    salvar(arquivo, alunos)

    carregados = carregar(arquivo)
    assert "2024001" in carregados
    aluno, notas = carregados["2024001"]
    assert aluno.nome == "Maria Silva"
    assert notas == (10.0, 10.0, 5.0)


def test_notas_sem_valor_viram_none(tmp_path):
    arquivo = tmp_path / "notas.csv"
    alunos = {
        "2024001": (Aluno("2024001", "Maria Silva"), (None, None, None)),
    }
    salvar(arquivo, alunos)

    _, notas = carregar(arquivo)["2024001"]
    assert notas == (None, None, None)
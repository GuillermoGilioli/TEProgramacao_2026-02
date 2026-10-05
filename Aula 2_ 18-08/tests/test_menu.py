from notas.menu import menu
from notas.servico import ServicoNotas


def test_menu_cadastra_lanca_e_lista(monkeypatch, capsys, tmp_path):
    servico = ServicoNotas(tmp_path / "notas.csv")
    entradas = iter(
        [
            "1", "2024001", "Maria Silva",
            "2", "2024001", "10", "10", "5",
            "4",
            "0",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    menu(servico)

    saida = capsys.readouterr().out
    assert "cadastrado" in saida
    assert "8.00" in saida
    assert "aprovado" in saida
    assert "MARIA SILVA" in saida.upper()
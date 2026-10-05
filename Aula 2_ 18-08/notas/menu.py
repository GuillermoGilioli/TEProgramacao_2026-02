"""Interface de linha de comando (menu interativo)."""

from .avaliacoes import calcular_media
from .classificacao import classificar
from .servico import ServicoNotas


def ler_numero(mensagem):
    """Lê um número do teclado, repetindo até ser válido."""
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Valor inválido. Digite um número, ex.: 7.5")


def cadastrar_aluno(servico):
    matricula = input("Matrícula: ").strip()
    nome = input("Nome: ").strip()
    try:
        servico.cadastrar_aluno(matricula, nome)
        print(f"Aluno {nome} ({matricula}) cadastrado com sucesso.")
    except ValueError as erro:
        print(f"Erro: {erro}")


def lancar_notas(servico):
    matricula = input("Matrícula do aluno: ").strip()
    nota1 = ler_numero("Nota da avaliação 1: ")
    nota2 = ler_numero("Nota da avaliação 2: ")
    nota3 = ler_numero("Nota da avaliação 3: ")
    try:
        servico.lancar_notas(matricula, nota1, nota2, nota3)
        media = calcular_media(nota1, nota2, nota3)
        print(f"Notas lançadas. Média: {media:.2f} -> {classificar(media)}")
    except ValueError as erro:
        print(f"Erro: {erro}")


def remover_aluno(servico):
    matricula = input("Matrícula do aluno a remover: ").strip()
    try:
        servico.remover_aluno(matricula)
        print(f"Aluno de matrícula {matricula} removido com sucesso.")
    except ValueError as erro:
        print(f"Erro: {erro}")


def listar_turma(servico):
    turma = servico.listar_turma()
    print(
        f"{'MATRÍCULA':<10}{'NOME':<22}{'N1':>6}{'N2':>6}{'N3':>6}"
        f"{'MÉDIA':>8}{'SITUAÇÃO':>12}"
    )
    print("-" * 70)
    for aluno in turma:
        n1, n2, n3 = aluno["notas"]
        n1 = f"{n1:.1f}" if n1 is not None else "-"
        n2 = f"{n2:.1f}" if n2 is not None else "-"
        n3 = f"{n3:.1f}" if n3 is not None else "-"
        media = f"{aluno['media']:.2f}" if aluno["media"] is not None else "-"
        print(
            f"{aluno['matricula']:<10}{aluno['nome']:<22}{n1:>6}{n2:>6}{n3:>6}"
            f"{media:>8}{aluno['situacao']:>12}"
        )
    print("=" * 70)


def menu(servico=None):
    """Executa o menu principal até o usuário escolher sair."""
    servico = servico or ServicoNotas()
    opcoes = {
        "1": ("Cadastrar aluno", cadastrar_aluno),
        "2": ("Lançar notas", lancar_notas),
        "3": ("Remover aluno", remover_aluno),
        "4": ("Listar turma", listar_turma),
    }
    while True:
        print("\n--- Sistema de Notas ---")
        for chave, (titulo, _) in opcoes.items():
            print(f"{chave} - {titulo}")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()
        if opcao == "0":
            print("Até mais!")
            return
        acao = opcoes.get(opcao)
        if acao is None:
            print("Opção inválida.")
            continue
        acao[1](servico)


def main():
    """Ponto de entrada do programa."""
    try:
        menu()
    except KeyboardInterrupt:
        print("\nAté mais!")
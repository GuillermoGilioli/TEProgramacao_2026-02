"""Orquestra as regras de negócio do sistema de notas."""

from . import persistencia
from .aluno import Aluno
from .avaliacoes import calcular_media, validar_nota
from .classificacao import classificar

SEM_NOTAS = (None, None, None)


class ServicoNotas:
    """Aplicação de notas: cadastro, lançamento e listagem da turma."""

    def __init__(self, arquivo="notas.csv"):
        self.arquivo = arquivo
        self.alunos = persistencia.carregar(arquivo)

    def cadastrar_aluno(self, matricula, nome):
        """Cadastra um novo aluno, garantindo matrícula única."""
        matricula = matricula.strip()
        if matricula in self.alunos:
            raise ValueError(f"A matrícula {matricula} já está cadastrada.")
        aluno = Aluno(matricula=matricula, nome=nome)
        self.alunos[aluno.matricula] = (aluno, SEM_NOTAS)
        persistencia.salvar(self.arquivo, self.alunos)

    def lancar_notas(self, matricula, nota1, nota2, nota3):
        """Lança as 3 avaliações de um aluno já cadastrado."""
        matricula = matricula.strip()
        try:
            aluno, _ = self.alunos[matricula]
        except KeyError:
            raise ValueError(f"Não há aluno com a matrícula {matricula}.")
        notas = (validar_nota(nota1), validar_nota(nota2), validar_nota(nota3))
        self.alunos[aluno.matricula] = (aluno, notas)
        persistencia.salvar(self.arquivo, self.alunos)

    def remover_aluno(self, matricula):
        """Remove aluno pelo número da matrícula."""
        matricula = matricula.strip()
        if matricula not in self.alunos:
            raise ValueError(f"Não há aluno com a matrícula {matricula}.")
        del self.alunos[matricula]
        persistencia.salvar(self.arquivo, self.alunos)

    def listar_turma(self):
        """Devolve a turma ordenada por matrícula, com média e situação."""
        turma = []
        for matricula, (aluno, notas) in sorted(self.alunos.items()):
            tem_notas = all(nota is not None for nota in notas)
            media = calcular_media(*notas) if tem_notas else None
            situacao = classificar(media) if tem_notas else "sem notas"
            turma.append(
                {
                    "matricula": matricula,
                    "nome": aluno.nome,
                    "notas": notas,
                    "media": media,
                    "situacao": situacao,
                }
            )
        return turma
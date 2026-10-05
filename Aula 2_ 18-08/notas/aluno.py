"""Modelo de aluno e regras de validação dos dados cadastrais."""

from dataclasses import dataclass


@dataclass
class Aluno:
    """Representa um aluno da disciplina.

    Atributos:
        matricula (str): código único de identificação do aluno.
        nome (str): nome completo do aluno.
    """

    matricula: str
    nome: str

    def __post_init__(self):
        self.matricula = self.matricula.strip()
        self.nome = self.nome.strip()
        if not self.matricula:
            raise ValueError("A matrícula não pode ser vazia.")
        if not self.nome:
            raise ValueError("O nome não pode ser vazio.")
import builtins
from dataclasses import dataclass
from operator import add, eq, ge, gt, le, lt, mul, ne, neg, not_, sub, truediv
from typing import TYPE_CHECKING

from .ctx import Ctx

if TYPE_CHECKING:
    from .ast import Block, Value

__all__ = [
    "add",
    "eq",
    "ge",
    "gt",
    "le",
    "lt",
    "mul",
    "ne",
    "neg",
    "not_",
    "print",
    "show",
    "sub",
    "truthy",
    "truediv",
]


class LoxReturn(Exception):
    """
    Exceção usada para implementar o comando 'return' do Lox.
    """
    def __init__(self, value: "Value"):
        super().__init__()
        self.value = value


@dataclass
class LoxFunction:
    """
    Representa uma função Lox em tempo de execução.
    Guarda os parâmetros, o corpo (AST) e o contexto (closure).
    """
    name: str
    params: list[str]
    body: "Block"
    ctx: Ctx

    def call(self, args: list["Value"]):
        """Executa a função com uma lista de argumentos."""
        # 1. Valida se o número de argumentos está correto
        if len(args) != len(self.params):
            raise TypeError(
                f"'{self.name}' esperava {len(self.params)} argumentos, mas recebeu {len(args)}."
            )

        # 2. Cria o ambiente de execução da chamada, combinando os parâmetros
        #    com os argumentos recebidos.
        local_env = dict(zip(self.params, args))

        # 3. Este novo ambiente local é aninhado dentro do contexto onde a função
        #    foi declarada (self.ctx), criando o closure.
        call_ctx = self.ctx.push(local_env)

        # 4. Executa o corpo da função, tratando a exceção de retorno.
        try:
            self.body.eval(call_ctx)
        except LoxReturn as ex:
            return ex.value
        
        # 5. Se a função terminar sem um 'return' explícito, ela retorna 'nil'.
        return None

    def __call__(self, *args):
        """Torna a função Lox chamável como uma função Python."""
        return self.call(list(args))


class LoxInstance:
    """
    Classe base para todos os objetos Lox.
    """


class LoxError(Exception):
    """
    Exceção para erros de execução Lox.
    """


nan = float("nan")
inf = float("inf")


def print(value: "Value"):
    """
    Imprime um valor lox.
    """
    builtins.print(show(value))


def show(value: "Value") -> str:
    """
    Converte valor lox para string.
    """
    return str(value)


def show_repr(value: "Value") -> str:
    """
    Mostra um valor lox, mas coloca aspas em strings.
    """
    if isinstance(value, str):
        return f'"{value}"'
    return show(value)


def truthy(value: "Value") -> bool:
    """
    Converte valor lox para booleano segundo a semântica do lox.
    """
    if value is None or value is False:
        return False
    return True
# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import numpy as np


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    N = None

    def __init__(self, board):
        self.board = board

    def __str__(self):
        return str(self.board).replace(' [', '').replace('[', '').replace(']', '')

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO
        return self.board[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""

        below = None
        if row < Board.N - 1:
            below = self.board[row + 1, col]

        above = None
        if row > 0:
            above = self.board[row - 1, col]

        return (below, above)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        left = None
        if col > 0:
            left = self.board[row, col - 1]

        right = None
        if col < Board.N - 1:
            right = self.board[row, col + 1]

        return (left, right)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        Board.N = int(stdin.readline())
        board = np.empty((0, Board.N), int)

        for i in range(Board.N):
            int_list = [ int(x) for x in stdin.readline().split('\t')] # i.e [2, 1, 2, 0]
            board = np.append(board, np.array([int_list]), axis=0)

        return Board(board)

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        super().__init__(TakuzuState(board))
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        board = state.board.board.copy()
        board[action[0], action[1]] = action[2]
        return TakuzuState(Board(board))

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        board = state.board

        # if len(np.where(board == 2)) == 0:
        #     return False

        for row in range(Board.N):
            for col in range(Board.N):
                number = board.get_number(row, col)
                if number == 2:
                    return False

        for col in range(Board.N):
            for row in range(Board.N):
                (left, right) = board.adjacent_horizontal_numbers(row, col)
                if (board.get_number(row, col) == left and left == right):
                    return False

        for row in range(Board.N):
            for col in range(Board.N):
                (below, above) = board.adjacent_vertical_numbers(row, col)
                if (board.get_number(row, col) == below and below == above):
                    return False

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()

    # Criar uma instância de Takuzu:
    problem = Takuzu(board)

    # Criar um estado com a configuração inicial:
    s0 = TakuzuState(board)
    print("Initial:\n", s0.board, sep="")

    # Aplicar as ações que resolvem a instância
    s1 = problem.result(s0, (0, 0, 0))
    s2 = problem.result(s1, (0, 2, 1))
    s3 = problem.result(s2, (1, 0, 1))
    s4 = problem.result(s3, (1, 1, 0))
    s5 = problem.result(s4, (1, 3, 1))
    s6 = problem.result(s5, (2, 0, 0))
    s7 = problem.result(s6, (2, 2, 1))
    s8 = problem.result(s7, (2, 3, 1))
    s9 = problem.result(s8, (3, 2, 0))

    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(s9))
    print("Solution:\n", s9.board, sep="")

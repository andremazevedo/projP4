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

    def get_board(self):
        """Devolve a representação interna do tabuleiro associada ao Estado."""
        return self.board




class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    N = None

    def __init__(self, matrix):
        self.matrix = matrix

    def __str__(self):
        return str(self.matrix).replace(' [', '').replace('[', '').replace(']', '')

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.matrix[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        below, above = None, None
        if row < Board.N - 1:
            below = self.matrix[row + 1, col]

        if row > 0:
            above = self.matrix[row - 1, col]

        return (below, above)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        left, right = None, None
        if col > 0:
            left = self.matrix[row, col - 1]

        if col < Board.N - 1:
            right = self.matrix[row, col + 1]

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
        matrix = np.empty((0, Board.N), int)

        for i in range(Board.N):
            int_list = [ int(x) for x in stdin.readline().split('\t')] # i.e [2, 1, 2, 0]
            matrix = np.append(matrix, np.array([int_list]), axis=0)

        return Board(matrix)

    # TODO: outros metodos da classe

    def domain(self, row: int, col: int):
        domain = [0, 1]
        for number in domain:

            below, above = self.adjacent_vertical_numbers(row, col)
            left, right = self.adjacent_horizontal_numbers(row, col)
            if left == number == right or below == number == above:
                domain.remove(number)
                break

            n_numbers_row = np.count_nonzero(self.matrix==number, axis=1)[row]
            n_numbers_col = np.count_nonzero(self.matrix==number, axis=0)[col]
            if n_numbers_row >= Board.N/2 or n_numbers_col >= Board.N/2:
                domain.remove(number)
                break

        return domain

    def result(self, action):
        left, right, number = action
        result_matrix = self.matrix.copy()
        result_matrix[left, right] = number
        return Board(result_matrix)

    def occurrences_test(self) -> bool:
        """Devolve true se o numero de 0s e 1s for igual para cada linha
        e coluna."""
        n_zeros_rows = np.count_nonzero(self.matrix==0, axis=1)#[1 1 1 1]
        n_ones_rows = np.count_nonzero(self.matrix==1, axis=1)#[1 0 0 2]

        n_zeros_cols = np.count_nonzero(self.matrix==0, axis=0)#[0 1 1 2]
        n_ones_cols = np.count_nonzero(self.matrix==1, axis=0)#[1 2 0 0]

        return np.array_equal(n_zeros_rows, n_ones_rows) and np.array_equal(n_zeros_cols, n_ones_cols)

    def unique_test(self) -> bool:
        """Devolve true se todas as linhas sao diferentes e se todas as
        colunas sao diferentes"""
        n_different_rows = np.unique(self.matrix, axis=0).shape[0]
        n_different_cols = np.unique(self.matrix.T, axis=0).shape[0]

        return n_different_rows == n_different_cols == Board.N



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
        board = state.get_board()
        possible_actions = []
        for row in range(Board.N):
            for col in range(Board.N):
                if board.get_number(row, col) == 2:
                    for number in board.domain(row, col):
                        possible_actions.append((row, col, number))

        # print(possible_actions)
        # quit()

        return possible_actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        result_board = state.get_board().result(action)
        return TakuzuState(result_board)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        board = state.get_board()

        for row in range(Board.N):
            for col in range(Board.N):
                number = board.get_number(row, col)
                below, above = board.adjacent_vertical_numbers(row, col)
                left, right = board.adjacent_horizontal_numbers(row, col)
                if number == 2 or below == number == above or left == number == right:
                    return False
    
        if not board.occurrences_test():
            return False

        if not board.unique_test():
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

    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)

    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")

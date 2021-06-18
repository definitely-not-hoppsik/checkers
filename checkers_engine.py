from typing import Union
import scanner as sc
import validation as vd


class Board:
    def __init__(self) -> None:
        self._b_piece = 'b'
        self._w_piece = 'w'
        self._board_length = 8
        self._board_width = 8
        self._piece_count = {self._b_piece: 0, self._w_piece: 0}
        self.board = []

    def _get_square(self, coords: tuple) -> str:
        x_coord, y_coord = coords
        return self.board[x_coord][y_coord]

    def _set_square(self, coords: tuple, value: str) -> None:
        x_coord, y_coord = coords
        self.board[x_coord][y_coord] = value

    @staticmethod
    def _get_mid_point(start_coords: tuple, end_coords: tuple) -> tuple:
        start_x, start_y = start_coords
        end_x, end_y = end_coords

        mid_point_coords = ((start_x + end_x)//2, (start_y + end_y)//2)

        return mid_point_coords

    def _add_piece(self, piece, coords) -> None:
        self._piece_count[piece] += 1
        self._set_square(coords, piece)

    def _remove_piece(self, coords) -> None:
        empty_square = None
        piece = self._get_square(coords)

        self._piece_count[piece] -= 1
        self._set_square(coords, empty_square)

    def _can_promote(self, piece: str, coords: tuple) -> bool:
        x_coord, _ = coords
        if (piece == 'b' and x_coord == 0) or (piece == 'w' and x_coord == 7):
            return True

        return False

    def _promote(self, piece: str, coords: tuple) -> None:
        assert piece == 'b' or piece == 'w'
        self._set_square(coords, piece.upper())

    def check_for_win(self) -> Union[None, str]:
        winner = None
        if 0 in self._piece_count:
            winner = list(self._piece_count.keys())[
                list(self._piece_count.values()).index(0)]

        return winner

    def _is_draw(self) -> bool:
        pass

    def create_empty_board(self) -> None:
        empty_square = None
        for _ in range(self._board_width):
            row = []
            for _ in range(self._board_length):
                row.append(empty_square)
            self.board.append(row)

    def set_starting_position(self) -> None:
        for i in range(self._board_width):
            for j in range(self._board_length):
                if i < 3:
                    if i % 2 == 0 and j % 2 == 1:
                        self._add_piece(self._w_piece, (i, j))
                    if i % 2 == 1 and j % 2 == 0:
                        self._add_piece(self._w_piece, (i, j))

                if i > 4:
                    if i % 2 == 1 and j % 2 == 0:
                        self._add_piece(self._b_piece, (i, j))
                    if i % 2 == 0 and j % 2 == 1:
                        self._add_piece(self._b_piece, (i, j))

    def print_board(self) -> None:
        for i in range(self._board_width):
            for j in range(self._board_length):
                square = self._get_square((i, j))
                if square is None:
                    print('_', end=' ')
                else:
                    print(square, end=' ')
            print()
        print()

    def move(self, start_coords: tuple, end_coords: tuple) -> None:

        piece = self._get_square(start_coords)
        empty_square = None

        if end_coords in sc.scan_for_move_coords(piece, start_coords):

            self._set_square(start_coords, empty_square)
            self._set_square(end_coords, piece)

        elif end_coords in sc.scan_for_capture_coords(piece, start_coords):
            mid_point_coords = self._get_mid_point(start_coords, end_coords)

            self._set_square(start_coords, empty_square)
            self._remove_piece(mid_point_coords)
            self._set_square(end_coords, piece)

        if self._can_promote(piece, end_coords):
            self._promote(piece, end_coords)


class Game:
    def __init__(self) -> None:
        self._board = Board()

    def _validate_input_decorator(func):
        def _validate_input(self) -> tuple:
            start_coords, end_coords = func(self)
            piece = self._board._get_square(start_coords)
            while True:
                if not vd.is_input_valid(piece, start_coords, end_coords):
                    print('Invalid input from validate input decorator')
                else:
                    break
            coords = (start_coords, end_coords)
            return coords

        return _validate_input

    def _force_jump_decorator(func):
        def _validate_input(self) -> tuple:
            while True:
                start_coords, end_coords = func(self)
                piece = self._board._get_square(start_coords)
                middle_coords = self._board._get_mid_point(
                    start_coords, end_coords)
                middle_piece = self._board._get_square(middle_coords)
                captures = vd.get_captures(piece, start_coords)
                if vd.is_capture_possible(piece, start_coords, middle_piece) == True:
                    if end_coords not in captures:
                        print('Invalid input from force jump decorator')
                else:
                    break

            coords = (start_coords, end_coords)
            return coords

        return _validate_input

    # @_force_jump_decorator
    # @_validate_input_decorator
    def _get_input(self) -> tuple:
        while True:
            try:
                start_coords = tuple(map(int, input().split()))
                end_coords = tuple(map(int, input().split()))
                break
            except ValueError:
                print('Invalid input while getting input')

        coords = (start_coords, end_coords)
        print('slfa', coords)

        return coords

    def _reset_game(self) -> None:
        self._board.create_empty_board()
        self._board.set_starting_position()

    def play(self) -> None:
        self._reset_game()
        winner = None

        while winner is None:
            winner = self._board.check_for_win()
            self._board.print_board()
            start_coords, end_coords = self._get_input()

            self._board.move(start_coords, end_coords)
            self._board.print_board()

        print(winner)


def main() -> None:
    game = Game()
    game.play()


if __name__ == "__main__":
    main()

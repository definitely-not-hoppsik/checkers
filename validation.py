import scanner as sc


def _is_in_board(coords: tuple) -> bool:
    x_coord, y_coord = tuple(map(int, coords))
    if 0 <= x_coord <= 7 and 0 <= y_coord <= 7:
        return True

    return False


def _is_piece_there(piece: str) -> bool:
    if piece is None:
        return False

    return True


def is_input_valid(piece: str, start_coords: tuple, end_coords: tuple) -> bool:

    if _is_in_board(start_coords) \
            and _is_in_board(end_coords) \
            and _is_piece_there(piece):
        return True

    return False


def get_captures(piece: str, start_coords) -> list:
    captures = sc.scan_for_capture_coords(piece, start_coords)

    return captures


def is_capture_possible(piece: str, start_coords) -> bool:
    captures = sc.scan_for_capture_coords(piece, start_coords)

    if not captures:
        return False

    return True

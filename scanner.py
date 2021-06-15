def scan_for_move_coords(piece: str, coords: tuple) -> list:
    x_coord, y_coord = coords
    possible_move_coords = []
    if piece in ('W', 'B'):
        possible_move_coords.append((x_coord-1, y_coord-1))
        possible_move_coords.append((x_coord+1, y_coord-1))
        possible_move_coords.append((x_coord-1, y_coord+1))
        possible_move_coords.append((x_coord+1, y_coord+1))

    elif piece == 'b':
        possible_move_coords.append((x_coord-1, y_coord-1))
        possible_move_coords.append((x_coord-1, y_coord+1))

    elif piece == 'w':
        possible_move_coords.append((x_coord+1, y_coord-1))
        possible_move_coords.append((x_coord+1, y_coord+1))

    return possible_move_coords


def scan_for_capture_coords(piece: str, coords: tuple) -> list:
    x_coord, y_coord = coords
    possible_capture_coords = []
    if piece in ('W', 'B'):
        possible_capture_coords.append((x_coord-2, y_coord-2))
        possible_capture_coords.append((x_coord+2, y_coord-2))
        possible_capture_coords.append((x_coord-2, y_coord+2))
        possible_capture_coords.append((x_coord+2, y_coord+2))

    elif piece == 'b':
        possible_capture_coords.append((x_coord-2, y_coord-2))
        possible_capture_coords.append((x_coord-2, y_coord+2))

    elif piece == 'w':
        possible_capture_coords.append((x_coord+2, y_coord-2))
        possible_capture_coords.append((x_coord+2, y_coord+2))

    return possible_capture_coords

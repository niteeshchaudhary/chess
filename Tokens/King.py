class King:
    def __init__(self, color):
        self.color = color
        self.has_moved = False

    def get_symbol(self):
        if self.color == "white":
            return "♔"
        else:
            return "♚"

    def get_possible_moves(self, board, position,is_check,game):
        row, col = position
        possible_moves = []

        # Define the eight possible move offsets for a king
        offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for offset in offsets:
            new_row, new_col = row + offset[0], col + offset[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    possible_moves.append((new_row, new_col))

        # Check for castling
        possible_moves.extend(self.get_castling_moves(board, position))

        if is_check:
            valid_moves = []
            for move in possible_moves:
                backup_board = [row[:] for row in board]
                game.make_move_on_board(position, move, backup_board)
                if not game.is_king_under_attack(move, backup_board):
                    valid_moves.append(move)

            return valid_moves
        else:
            return possible_moves

    def get_castling_moves(self, board, position):
        castling_moves = []
        row, col = position

        # Check for kingside castling
        if not self.has_moved:
            rook_col = 7 if self.color == "white" else 7
            if (
                board[row][col + 1] is None
                and board[row][col + 2] is None
                and board[row][rook_col] is not None
                and isinstance(board[row][rook_col], Rook)
                and not board[row][rook_col].has_moved
            ):
                castling_moves.append((row, col + 2))

        # Check for queenside castling
        if not self.has_moved:
            rook_col = 0 if self.color == "white" else 0
            if (
                board[row][col - 1] is None
                and board[row][col - 2] is None
                and board[row][col - 3] is None
                and board[row][rook_col] is not None
                and isinstance(board[row][rook_col], Rook)
                and not board[row][rook_col].has_moved
            ):
                castling_moves.append((row, col - 2))

        return castling_moves
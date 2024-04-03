class Queen:
    def __init__(self, color):
        self.color = color

    def get_symbol(self):
        if self.color == "white":
            return "♕"
        else:
            return "♛"

    def get_possible_moves(self, board, position,is_check,game):
        row, col = position
        possible_moves = []

        # Check horizontals
        for c in range(col + 1, 8):
            if board[row][c] is None:
                possible_moves.append((row, c))
            else:
                if board[row][c].color != self.color:
                    possible_moves.append((row, c))
                break

        for c in range(col - 1, -1, -1):
            if board[row][c] is None:
                possible_moves.append((row, c))
            else:
                if board[row][c].color != self.color:
                    possible_moves.append((row, c))
                break

        # Check verticals
        for r in range(row + 1, 8):
            if board[r][col] is None:
                possible_moves.append((r, col))
            else:
                if board[r][col].color != self.color:
                    possible_moves.append((r, col))
                break

        for r in range(row - 1, -1, -1):
            if board[r][col] is None:
                possible_moves.append((r, col))
            else:
                if board[r][col].color != self.color:
                    possible_moves.append((r, col))
                break

        # Check diagonals
        for offset in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            current_row, current_col = row + offset[0], col + offset[1]
            while 0 <= current_row < 8 and 0 <= current_col < 8:
                if board[current_row][current_col] is None:
                    possible_moves.append((current_row, current_col))
                elif board[current_row][current_col].color != self.color:
                    possible_moves.append((current_row, current_col))
                    break  # Can't move further in this direction
                else:
                    break  # Can't capture own piece

                current_row += offset[0]
                current_col += offset[1]

        if is_check:
            valid_moves = []
            king_position = game.find_king_position(self.color)
            for move in possible_moves:
                backup_board = [row[:] for row in board]
                game.make_move_on_board(position, move, backup_board)
                if not game.is_king_under_attack(king_position, backup_board):
                    valid_moves.append(move)

            return valid_moves
        else:
            return possible_moves
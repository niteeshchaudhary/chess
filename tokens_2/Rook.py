class Rook:
    def __init__(self, color):
        self.name="rook"
        self.color = color
        self.has_moved=False

    def get_symbol(self):
        if self.color == "white":
            return "♖"
        else:
            return "♜"
        
    def get_possible_moves_op(self, board, position, is_check, game):
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
            

        return possible_moves

    def get_possible_moves(self, board, position, is_check,game):
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
            
        valid_moves = []
        king_position = game.find_king_position(self.color)
        for move in possible_moves:
            backup_board = [row[:] for row in board]
            game.make_move_on_board(position, move, backup_board)
            if not game.is_king_under_attack(king_position, backup_board):
                valid_moves.append(move)

        return valid_moves

class Knight:
    def __init__(self, color):
        self.color = color

    def get_symbol(self):
        if self.color == "white":
            return "♘"
        else:
            return "♞"
        
    def get_possible_moves_op(self, board, position,is_check,game):
        row, col = position
        possible_moves = []

        # Define the eight possible move offsets for a knight
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for offset in offsets:
            new_row, new_col = row + offset[0], col + offset[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    possible_moves.append((new_row, new_col))
        
        return possible_moves

    def get_possible_moves(self, board, position,is_check,game):
        row, col = position
        possible_moves = []

        # Define the eight possible move offsets for a knight
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for offset in offsets:
            new_row, new_col = row + offset[0], col + offset[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    possible_moves.append((new_row, new_col))

        if is_check:
            valid_moves = []
            colorcheck="black" if self.color=="white" else "white"
            print("Knight : ", self.color)
            king_position = game.find_king_position(self.color)
            for move in possible_moves:
                backup_board = [row[:] for row in board]
                game.make_move_on_board(position, move, backup_board)
                if not game.is_king_under_attack(king_position, backup_board):
                    valid_moves.append(move)

            return valid_moves
        else:
            return possible_moves
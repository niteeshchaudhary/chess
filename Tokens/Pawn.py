class Pawn:
    def __init__(self, color):
        self.color = color
        self.direction = 1 if color == "white" else -1
        self.en_passant_target=None
        
    def get_symbol(self):
        if self.color == "white":
            return "♙"
        else:
            return "♟"
        
    def get_possible_moves_op(self, board, position,is_check,game):
        row, col = position
        possible_moves = []

        # Check for forward move
        forward_row = row + self.direction

        # Check for captures
        for offset in [-1, 1]:
            capture_row = row + self.direction
            capture_col = col + offset
            if (
                0 <= capture_row < 8
                and 0 <= capture_col < 8
                # and board[capture_row][capture_col] != None
                # and board[capture_row][capture_col].color != self.color
            ):
                print(board[capture_row][capture_col])
                possible_moves.append((capture_row, capture_col))


        return possible_moves

    def get_possible_moves(self, board, position,is_check,game):
        row, col = position
        possible_moves = []

        # Check for forward move
        forward_row = row + self.direction
        if 0 <= forward_row < 8 and board[forward_row][col] == None:
            possible_moves.append((forward_row, col))

            # Check for double move from starting position
            if (self.color == "white" and row == 1) or (self.color == "black" and row == 6):
                double_forward_row = row + 2 * self.direction
                if board[double_forward_row][col] == None:
                    possible_moves.append((double_forward_row, col))
                    self.en_passant_target = (row + self.direction, col)  # Set en passant target

        # Check for captures
        for offset in [-1, 1]:
            capture_row = row + self.direction
            capture_col = col + offset
            if (
                0 <= capture_row < 8
                and 0 <= capture_col < 8
                and board[capture_row][capture_col] != None
                and board[capture_row][capture_col].color != self.color
            ):
                print(board[capture_row][capture_col])
                possible_moves.append((capture_row, capture_col))

        print("enpi",game.en_passant_target)
        # Check for en passant capture
        if game.en_passant_target:
            en_passant_row, en_passant_col = game.en_passant_target
            print("enpi enter",game.en_passant_target)
            for offset in [-1, 1]:
                capture_row = row + self.direction
                capture_col = col + offset
                print("enpi enter ye ",(capture_row, capture_col),game.en_passant_target)
                if (capture_row, capture_col) == game.en_passant_target:
                    print("why")
                    possible_moves.append((en_passant_row, capture_col))

        # Check for pawn promotion
        if (self.color == "white" and forward_row == 7) or (self.color == "black" and forward_row == None):
            possible_moves = [(move, "promote") for move in possible_moves]

        print(possible_moves)
        if is_check:
            valid_moves = []
            king_position = game.find_king_position(self.color)
            for move in possible_moves:
                backup_board = [row[:] for row in board]
                game.make_move_on_board(position, move, backup_board)
                if not game.is_king_under_attack(king_position, backup_board):
                    print("here is the move ",move)
                    valid_moves.append(move)

            return valid_moves
        else:
            return possible_moves
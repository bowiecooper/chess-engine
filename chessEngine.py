#this class is responsible for storing all information about the current state of a chess game
#also responsible for determining the valid moves at the current state
#will also keep a move log


class game_state():
    def __init__(self):
        #board is an 8x8 2D list where each element of the list has 2 characters
        #"--" represents an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "wp", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "wN", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = [] 
        self.move_functions = {'p' : self.get_pawn_moves, 'R' : self.get_rook_moves, 'N' : self.get_knight_moves,
                              'B' : self.get_bishop_moves, 'Q' : self.get_queen_moves, 'K' : self.get_king_moves}       
    
    #takes in a move as input and executes it - doesn't work for en passant or castling
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) 
        self.white_to_move = not self.white_to_move #take turns
        
    #undo the last move
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
    
    
    '''
    all moves with considering checks
    '''
    def get_all_valid_moves(self):
        return self.get_all_possible_moves()

    '''
    all moves without considering checks
    '''
    def get_all_possible_moves(self):
        moves = [move((6, 4), (4, 4), self.board)]
        for row in range(len(self.board)): #number of rows
            for col in range(len(self.board[row])): #number of cols in given row
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move): #if piece is white and whites turn to move we should look at this piece
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves) #calls appropiate move function
        return moves
                    
    

    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:
            # Forward move by 1
            if row - 1 >= 0 and self.board[row - 1][col] == '--':
                moves.append(move((row, col), (row - 1, col), self.board))
                # Forward move by 2 from starting position
                if row == 6 and self.board[row - 2][col] == '--':
                    moves.append(move((row, col), (row - 2, col), self.board))
            # Capture left
            if row - 1 >= 0 and col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(move((row, col), (row - 1, col - 1), self.board))
            # Capture right
            if row - 1 >= 0 and col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(move((row, col), (row - 1, col + 1), self.board))
        else:
            # Forward move by 1
            if row + 1 <= 7 and self.board[row + 1][col] == '--':
                moves.append(move((row, col), (row + 1, col), self.board))
                # Forward move by 2 from starting position
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(move((row, col), (row + 2, col), self.board))
            # Capture left
            if row + 1 <= 7 and col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(move((row, col), (row + 1, col - 1), self.board))
            # Capture right
            if row + 1 <= 7 and col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(move((row, col), (row + 1, col + 1), self.board))
                
        #add pawn promotions later
    
    
    
    #get all rook moves
    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: #then we're on the board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break
        
                
            
        
    #get all bishop moves
    def get_bishop_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: #on the board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break
                        
        
        
    #get all knight moves
    def get_knight_moves(self, row, col, moves):
        directions = ((-2, -1), (-2, 1), (2, 1), (2, -1), (1, -2), (1, 2), (-1, 2), (-1, -2))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == '--' or end_piece[0] == enemy_color:
                    moves.append(move((row, col), (end_row, end_col), self.board))
        
        
    #get all queen moves
    def get_queen_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))  
        enemy_color = 'b' if self.white_to_move else 'w'          
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: #on the board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break  
        
        
    #get all king moves
    def get_king_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))  
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8: #on the board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--' or end_piece[0] == enemy_color:
                        moves.append(move((row, col), (end_row, end_col), self.board))
                           
                             
                    
class move():
    
    #maps keys to values
    
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}
    
    
    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_ID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, move):
            return self.move_ID == other.move_ID
        return False
    
        
    def get_chess_notation(self):
        #could make this like real chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]



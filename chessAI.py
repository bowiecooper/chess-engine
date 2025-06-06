#AI for chess 
import random

# piece_scores = {"K": 0, "Q" : 9, "B" : 3, "N" : 3, "p" : 1, "R" : 5}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


def find_random_move(valid_moves):
    print("making random moves")
    return valid_moves[random.randint(0, len(valid_moves) - 1)]
        



#def find_best_move_old(gs, valid_moves):
    # turn_multiplier = 1 if gs.white_to_move else -1
    
    # opponent_min_max_score = CHECKMATE
    # best_player_move = None
    # random.shuffle(valid_moves)
    # for player_move in valid_moves:
    #     gs.make_move(player_move)
    #     opponents_moves = gs.get_all_valid_moves()
    #     if gs.stalemate:
    #         opponent_max_score = STALEMATE
    #     elif gs.checkmate:
    #         opponent_max_score = -CHECKMATE
    #     else:
    #         opponent_max_score = -CHECKMATE
        
    #     opponent_max_score = -CHECKMATE
    #     for opponents_move in opponents_moves:
    #         gs.make_move(opponents_move)
    #         gs.get_all_valid_moves()
    #         if gs.checkmate:
    #             score = CHECKMATE
    #         elif gs.stalemate:
    #             score = STALEMATE
    #         else:
    #             score = -turn_multiplier * score_material(gs.board)
    #         if score > opponent_max_score:
    #             opponent_max_score = score
    #         gs.undo_move()
    #     if opponent_max_score < opponent_min_max_score:
    #         opponent_min_max_score = opponent_max_score
    #         best_player_move = player_move
    #     gs.undo_move()
    # return best_player_move



def find_best_move(gs, valid_moves):
    global next_move
    next_move = None
    find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1)
    return next_move

#def find_move_min_max(gs, valid_moves, depth, white_to_move):
    # global next_move
    # if depth == 0:
    #     return score_material(gs.board)

    # if white_to_move:
    #     max_score = -CHECKMATE
    #     for move in valid_moves:
    #         gs.make_move(move)
    #         next_moves = gs.get_all_valid_moves()

    #         # 🔥 Handle terminal game state
    #         if gs.checkmate:
    #             score = CHECKMATE
    #         elif gs.stalemate:
    #             score = STALEMATE
    #         else:
    #             score = find_move_min_max(gs, next_moves, depth - 1, False)

    #         gs.undo_move()

    #         if score > max_score:
    #             max_score = score
    #             if depth == DEPTH:
    #                 next_move = move
    #     return max_score
    # else:
    #     min_score = CHECKMATE
    #     for move in valid_moves:
    #         gs.make_move(move)
    #         next_moves = gs.get_all_valid_moves()

    #         if gs.checkmate:
    #             score = -CHECKMATE
    #         elif gs.stalemate:
    #             score = STALEMATE
    #         else:
    #             score = find_move_min_max(gs, next_moves, depth - 1, True)

    #         gs.undo_move()

    #         if score < min_score:
    #             min_score = score
    #             if depth == DEPTH:
    #                 next_move = move
    #     return min_score


def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    #looking for a maximum and multiply by negative one on black turn
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(gs)
    
    random.shuffle(valid_moves)
    max_score = -CHECKMATE
    
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_all_valid_moves()
        
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = 0
        else:
            score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
                
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
                
        gs.undo_move()
        alpha = max(alpha, max_score)
        
        if alpha >= beta:
            break
    return max_score

def score_board(gs):
    """
    Simple chess evaluation: material + basic position + simple threats
    """
    CHECKMATE = 1000
    STALEMATE = 0
    
    if gs.checkmate:
        return -CHECKMATE if gs.white_to_move else CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    
    # Piece values
    piece_values = {'p': 100, 'R': 500, 'N': 320, 'B': 330, 'Q': 900, 'K': 0}
    
    score = 0
    
    # Material and basic positional evaluation
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece != '--':
                color = piece[0]
                piece_type = piece[1]
                value = piece_values[piece_type]
                
                # Add positional bonus
                pos_bonus = get_position_bonus(piece_type, row, col, color)
                
                if color == 'w':
                    score += value + pos_bonus
                else:
                    score -= value + pos_bonus
    
    # Simple king safety
    score += evaluate_king_safety_simple(gs)
    
    # Check for hanging pieces (pieces under attack and not defended)
    score += evaluate_hanging_pieces(gs)
    
    return score

def get_position_bonus(piece_type, row, col, color):
    """Simple positional bonuses"""
    bonus = 0
    
    # Center control bonus for all pieces
    center_distance = abs(3.5 - row) + abs(3.5 - col)
    bonus += int((7 - center_distance) * 2)
    
    # Piece-specific bonuses
    if piece_type == 'p':
        # Pawns advance bonus
        if color == 'w':
            bonus += (6 - row) * 5  # White pawns moving up
        else:
            bonus += (row - 1) * 5  # Black pawns moving down
    
    elif piece_type == 'N':
        # Knights on rim are dim
        if row == 0 or row == 7 or col == 0 or col == 7:
            bonus -= 20
    
    elif piece_type == 'K':
        # King safety - stay back in middlegame
        if color == 'w' and row < 6:
            bonus -= 30
        elif color == 'B' and row > 1:
            bonus -= 30
    
    return bonus

def evaluate_king_safety_simple(gs):
    """Very simple king safety check"""
    score = 0
    
    # Just check if king is in check (basic safety)
    if gs.in_check_flag:
        score -= 50 if gs.white_to_move else 50
    
    return score

def evaluate_hanging_pieces(gs):
    """Find pieces that are attacked but not defended"""
    score = 0
    piece_values = {'p': 100, 'R': 500, 'N': 320, 'B': 330, 'Q': 900, 'K': 0}
    
    # Get all opponent moves to see what they're attacking
    original_turn = gs.white_to_move
    
    # Check white pieces being attacked by black
    gs.white_to_move = False
    black_attacks = get_attacked_squares(gs)
    gs.white_to_move = True
    white_defends = get_attacked_squares(gs)
    
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece != '--' and piece[0] == 'w':
                if (row, col) in black_attacks and (row, col) not in white_defends:
                    score -= piece_values[piece[1]] // 2  # Hanging piece penalty
    
    # Check black pieces being attacked by white  
    gs.white_to_move = True
    white_attacks = get_attacked_squares(gs)
    gs.white_to_move = False
    black_defends = get_attacked_squares(gs)
    
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece != '--' and piece[0] == 'B':
                if (row, col) in white_attacks and (row, col) not in black_defends:
                    score += piece_values[piece[1]] // 2  # Hanging piece bonus
    
    gs.white_to_move = original_turn
    return score

def get_attacked_squares(gs):
    """Get set of squares attacked by current player"""
    attacked = set()
    moves = gs.get_all_possible_moves()
    for move in moves:
        attacked.add((move.end_row, move.end_col))
    return attacked
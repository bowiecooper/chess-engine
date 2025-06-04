#driver file - handles user input and displaying the current GameState object.
import chessEngine
import pygame as p

p.init()
WIDTH = 512
HEIGHT = 512 
DIMENSION = 8 
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
load images will initialize a global dictionary of images. called exactly once in main
'''
def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bQ", "bK", "bB"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #access an image by calling IMAGES['wp']

'''
main driver for code. handle user input and updating graphics
'''
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.game_state()
    valid_moves = gs.get_all_valid_moves()
    move_made = False #flag variable for when a move is made
    load_images() #only do once
    running = True
    animate = False
    sq_selected = () #no square is selected initially - keeps track of last click of the user (tuple: (row, col))
    playerClicks = [] #keeps track of player clicks EX: move pawn up two spaces (two tuples: [6, 4), (4, 4)])
    game_over = False
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos() #(x,y) location of the mouse
                    col = location[0] // SQ_SIZE 
                    row = location[1] // SQ_SIZE 
                    if sq_selected == (row, col): #user clicked the same square twice
                        sq_selected = () #reset the selection
                        playerClicks = []
                    else:
                        sq_selected = (row, col)
                        playerClicks.append(sq_selected) #append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #after 2nd click
                        # Check if this is an en passant move
                        is_enpassant = False
                        if gs.board[playerClicks[0][0]][playerClicks[0][1]][1] == 'p':  # If it's a pawn
                            if playerClicks[1] == gs.enpassant_possible:  # If the end square is the en passant square
                                is_enpassant = True
                        
                        is_castle_move = False
                        if gs.board[playerClicks[0][0]][playerClicks[0][1]][1] == 'K':
                            if playerClicks[1] == (playerClicks[0][0], playerClicks[0][1] + 2) or playerClicks[1] == (playerClicks[0][0], playerClicks[0][1] - 2):
                                is_castle_move = True
                        move = chessEngine.move(playerClicks[0], playerClicks[1], gs.board, is_enpassant_move=is_enpassant, is_castle_move=is_castle_move)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(move)
                                move_made = True
                                animate = True
                                sq_selected = ()
                                playerClicks = []
                        if not move_made:
                            playerClicks = [sq_selected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True
                    animate = False
                if e.key == p.K_r:
                    gs = chessEngine.game_state()
                    valid_moves = gs.get_all_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    
        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_all_valid_moves()
            move_made = False
            animate = False
             
        draw_game_state(screen, gs, valid_moves, sq_selected)  # Draw the game state

        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                draw_text(screen, 'Black wins by checkmate')
            else:
                draw_text(screen, 'White wins by checkmate')
        elif gs.stalemate:
            game_over = True
            draw_text(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()

#highlight square selected

def highlight_square(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        row, col = sq_selected
        if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'): #sq selected is a piece that can be moved
            #highligh selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('cyan'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))



                
'''
Responsible for all the graphics within a current game state
'''                           
def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen) #draw squares on the board
    highlight_square(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board) #draw pieces on top of those square
    
'''
Draw squares on the board
'''
def draw_board(screen):
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
           

'''
Draw the pieces on the board using current GameState.board
'''
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--": #not empty so we want to draw
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)) #can ignore blit error

def animate_move(move, screen, board, clock):
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row*frame/frame_count, move.start_col + d_col*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)
        screen.blit(IMAGES[move.piece_moved], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(120)
    

    
def draw_text(screen, text):
    font = p.font.SysFont("Times New Roman", 32, True, False)
    text_object = font.render(text, 0, p.Color('Gray'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color("Black"))
    screen.blit(text_object, text_location.move(2, 2))

if __name__ == "__main__":
    main()


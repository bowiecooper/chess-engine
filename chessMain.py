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
    sq_selected = () #no square is selected initially - keeps track of last click of the user (tuple: (row, col))
    playerClicks = [] #keeps track of player clicks EX: move pawn up two spaces (two tuples: [6, 4), (4, 4)])
    
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    move = chessEngine.move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        sq_selected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sq_selected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True
                    
        if move_made:
            valid_moves = gs.get_all_valid_moves()
            move_made = False
             
        draw_game_state(screen, gs)  # Draw the game state
        clock.tick(MAX_FPS)
        p.display.flip()
                
'''
Responsible for all the graphics within a current game state
'''                           
def draw_game_state(screen, gs):
    draw_board(screen) #draw squares on the board
    draw_pieces(screen, gs.board) #draw pieces on top of those square
    
'''
Draw squares on the board
'''
def draw_board(screen):
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
    
    
    
if __name__ == "__main__":
    main()


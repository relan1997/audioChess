# two player chess in python with Pygame!
# part one, set up variables images and game loop

import sounddevice as sd
import string
from scipy.io.wavfile import write
import whisper
import numpy as np
import pygame
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Load whisper once
whisper_model = whisper.load_model("base")

# Mic button position
suggestion_button_rect = pygame.Rect(850, 700, 100, 40)
show_suggestion = False
suggested_piece = None
suggested_move = None
def clear_suggestion():
    global show_suggestion, suggested_piece, suggested_move
    show_suggestion = False
    suggested_piece = None
    suggested_move = None



mic_button_rect = pygame.Rect(850, 750, 100, 40)


pygame.init()
black_turn_sound = pygame.mixer.Sound("blackTurn.wav")
white_turn_sound = pygame.mixer.Sound("whiteTurn.wav")
error_sound = pygame.mixer.Sound("error.wav")
suggestion_sound = pygame.mixer.Sound("suggestion.wav")
black_win_sound = pygame.mixer.Sound("blackWins.wav")
white_win_sound = pygame.mixer.Sound("whiteWins.wav")
WIDTH = 1000
HEIGHT = 900
file_to_index = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}
rank_to_index = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7
}
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60
# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
#its value is equal to the value of the piece selected from the index in the white or black pieces list
# 100 is a dummy value to indicate no piece selected
valid_moves = []
clear_suggestion()
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False
def draw_board():
    # Draw the chess board squares
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
    
    # Draw status area
    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
    pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
    
    # Draw status text
    status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                   'Black: Select a Piece to Move!', 'Black: Select a Destination!']
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
    
    # Draw grid lines
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
    
    # Draw file labels (a-h) at the bottom
    small_font = pygame.font.Font('freesansbold.ttf', 20)
    for i in range(8):
        file_label = chr(97 + i)  # 'a' is ASCII 97
        screen.blit(small_font.render(file_label, True, 'black'), (i * 100 + 85, 780))
    
    # Draw rank labels (1-8) on the left
    for i in range(8):
        rank_label = str(8 - i)  # Top row is 8, bottom row is 1
        screen.blit(small_font.render(rank_label, True, 'black'), (5, i * 100 + 5))
    
    screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))

        # Draw Suggestion Button
    # Draw Suggestion Button (neater design)
    button_color = (255, 200, 60) if show_suggestion else (230, 230, 230)
    border_color = (200, 140, 0)
    shadow_color = (180, 180, 180)

# Draw shadow
    pygame.draw.rect(screen, shadow_color, (suggestion_button_rect.x+3, suggestion_button_rect.y+3, suggestion_button_rect.width, suggestion_button_rect.height), border_radius=12)
# Draw button
    pygame.draw.rect(screen, button_color, suggestion_button_rect, border_radius=12)
# Draw border
    pygame.draw.rect(screen, border_color, suggestion_button_rect, 3, border_radius=12)

    label_color = (80, 50, 0) if show_suggestion else (60, 60, 60)
    label = font.render('SUGGEST', True, label_color)
    label_rect = label.get_rect(center=suggestion_button_rect.center)
    screen.blit(label, label_rect)




# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                  100, 100], 2)
        # Draw suggestion highlight if enabled
    if show_suggestion and suggested_piece is not None and suggested_move is not None:
        if turn_step < 2:
            pos = white_locations[suggested_piece]
            pygame.draw.rect(screen, 'orange', [pos[0]*100+1, pos[1]*100+1, 100, 100], 4)
            move = suggested_move
            pygame.draw.rect(screen, 'orange', [move[0]*100+1, move[1]*100+1, 100, 100], 4)
        else:
            pos = black_locations[suggested_piece]
            pygame.draw.rect(screen, 'orange', [pos[0]*100+1, pos[1]*100+1, 100, 100], 4)
            move = suggested_move
            pygame.draw.rect(screen, 'orange', [move[0]*100+1, move[1]*100+1, 100, 100], 4)



# function to check all pieces valid options on board

# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white': #position[0] == x && position[1] == y
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1: #the left line says pawn is at its starting position
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def evaluate_board(w_pieces, b_pieces):
    piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 1000}
    white_score = sum(piece_values[p] for p in w_pieces)
    black_score = sum(piece_values[p] for p in b_pieces)
    return white_score - black_score

def get_all_moves(pieces, locations, color):
    moves = []
    for i, piece in enumerate(pieces):
        pos = locations[i]
        if piece == 'pawn':
            valid = check_pawn(pos, color)
        elif piece == 'knight':
            valid = check_knight(pos, color)
        elif piece == 'bishop':
            valid = check_bishop(pos, color)
        elif piece == 'rook':
            valid = check_rook(pos, color)
        elif piece == 'queen':
            valid = check_queen(pos, color)
        elif piece == 'king':
            valid = check_king(pos, color)
        else:
            valid = []
        for move in valid:
            moves.append((i, move))
    return moves

def minimax(depth, alpha, beta, maximizingPlayer, w_pieces, w_locs, b_pieces, b_locs):
    if depth == 0 or 'king' not in w_pieces or 'king' not in b_pieces:
        return evaluate_board(w_pieces, b_pieces)
    if maximizingPlayer:
        maxEval = float('-inf')
        moves = get_all_moves(w_pieces, w_locs, 'white')
        for i, move in moves:
            w_p, w_l, b_p, b_l = w_pieces[:], w_locs[:], b_pieces[:], b_locs[:]
            old_pos = w_l[i]
            w_l[i] = move
            if move in b_l:
                captured = b_l.index(move)
                b_p.pop(captured)
                b_l.pop(captured)
            eval = minimax(depth-1, alpha, beta, False, w_p, w_l, b_p, b_l)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            w_l[i] = old_pos
        return maxEval
    else:
        minEval = float('inf')
        moves = get_all_moves(b_pieces, b_locs, 'black')
        for i, move in moves:
            w_p, w_l, b_p, b_l = w_pieces[:], w_locs[:], b_pieces[:], b_locs[:]
            old_pos = b_l[i]
            b_l[i] = move
            if move in w_l:
                captured = w_l.index(move)
                w_p.pop(captured)
                w_l.pop(captured)
            eval = minimax(depth-1, alpha, beta, True, w_p, w_l, b_p, b_l)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
            b_l[i] = old_pos
        return minEval

def evaluate_board(w_pieces, b_pieces):
    piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 1000}
    white_score = sum(piece_values[p] for p in w_pieces)
    black_score = sum(piece_values[p] for p in b_pieces)
    return white_score - black_score

def get_all_moves(pieces, locations, color):
    moves = []
    for i, piece in enumerate(pieces):
        pos = locations[i]
        if piece == 'pawn':
            valid = check_pawn(pos, color)
        elif piece == 'knight':
            valid = check_knight(pos, color)
        elif piece == 'bishop':
            valid = check_bishop(pos, color)
        elif piece == 'rook':
            valid = check_rook(pos, color)
        elif piece == 'queen':
            valid = check_queen(pos, color)
        elif piece == 'king':
            valid = check_king(pos, color)
        else:
            valid = []
        for move in valid:
            moves.append((i, move))
    return moves

def minimax(depth, alpha, beta, maximizingPlayer, w_pieces, w_locs, b_pieces, b_locs):
    if depth == 0 or 'king' not in w_pieces or 'king' not in b_pieces:
        return evaluate_board(w_pieces, b_pieces)
    if maximizingPlayer:
        maxEval = float('-inf')
        moves = get_all_moves(w_pieces, w_locs, 'white')
        for i, move in moves:
            w_p, w_l, b_p, b_l = w_pieces[:], w_locs[:], b_pieces[:], b_locs[:]
            old_pos = w_l[i]
            w_l[i] = move
            if move in b_l:
                captured = b_l.index(move)
                b_p.pop(captured)
                b_l.pop(captured)
            eval = minimax(depth-1, alpha, beta, False, w_p, w_l, b_p, b_l)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            w_l[i] = old_pos
        return maxEval
    else:
        minEval = float('inf')
        moves = get_all_moves(b_pieces, b_locs, 'black')
        for i, move in moves:
            w_p, w_l, b_p, b_l = w_pieces[:], w_locs[:], b_pieces[:], b_locs[:]
            old_pos = b_l[i]
            b_l[i] = move
            if move in w_l:
                captured = w_l.index(move)
                w_p.pop(captured)
                w_l.pop(captured)
            eval = minimax(depth-1, alpha, beta, True, w_p, w_l, b_p, b_l)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
            b_l[i] = old_pos
        return minEval

def suggest_move():
    global suggested_piece, suggested_move
    depth = 5
    best_score = float('-inf') if turn_step < 2 else float('inf')
    best_move = None
    if turn_step < 2:
        moves = get_all_moves(white_pieces, white_locations, 'white')
        for i, move in moves:
            w_p, w_l, b_p, b_l = white_pieces[:], white_locations[:], black_pieces[:], black_locations[:]
            old_pos = w_l[i]
            w_l[i] = move
            if move in b_l:
                captured = b_l.index(move)
                b_p.pop(captured)
                b_l.pop(captured)
            score = minimax(depth-1, float('-inf'), float('inf'), False, w_p, w_l, b_p, b_l)
            if score > best_score:
                best_score = score
                best_move = (i, move)
            w_l[i] = old_pos
        if best_move:
            suggested_piece, suggested_move = best_move
    else:
        moves = get_all_moves(black_pieces, black_locations, 'black')
        for i, move in moves:
            w_p, w_l, b_p, b_l = white_pieces[:], white_locations[:], black_pieces[:], black_locations[:]
            old_pos = b_l[i]
            b_l[i] = move
            if move in w_l:
                captured = w_l.index(move)
                w_p.pop(captured)
                w_l.pop(captured)
            score = minimax(depth-1, float('-inf'), float('inf'), True, w_p, w_l, b_p, b_l)
            if score < best_score:
                best_score = score
                best_move = (i, move)
            b_l[i] = old_pos
        if best_move:
            suggested_piece, suggested_move = best_move
    suggestion_sound.play()


# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options



def handle_click(click_coords):
    print(click_coords)
    global selection, turn_step, valid_moves, winner, game_over
    if turn_step <= 1:
        if click_coords == (8, 8) or click_coords == (9, 8):
            winner = 'black'
            black_win_sound.play()

        # 🆕 If clicked a valid move square
        if click_coords in valid_moves and selection != 100:
            white_locations[selection] = click_coords
            if click_coords in black_locations:
                black_piece = black_locations.index(click_coords)
                captured_pieces_white.append(black_pieces[black_piece])
                if black_pieces[black_piece] == 'king':
                    winner = 'white'
                    white_win_sound.play()
                black_pieces.pop(black_piece)
                black_locations.pop(black_piece)
            turn_step = 2
            print("audio Played")
            black_turn_sound.play()
            selection = 100
            valid_moves = []

        # 🆕 If clicked a new selectable white piece
        elif click_coords in white_locations:
            new_selection = white_locations.index(click_coords)
            selection = new_selection
            valid_moves = check_valid_moves()
            if turn_step == 0:
                turn_step = 1

    elif turn_step > 1:
        if click_coords == (8, 8) or click_coords == (9, 8):
            winner = 'white'
            white_win_sound.play()

        if click_coords in valid_moves and selection != 100:
            black_locations[selection] = click_coords
            if click_coords in white_locations:
                white_piece = white_locations.index(click_coords)
                captured_pieces_black.append(white_pieces[white_piece])
                if white_pieces[white_piece] == 'king':
                    winner = 'black'
                white_pieces.pop(white_piece)
                white_locations.pop(white_piece)
            turn_step = 0
            selection = 100
            valid_moves = []

        elif click_coords in black_locations:
            new_selection = black_locations.index(click_coords)
            selection = new_selection
            valid_moves = check_valid_moves()
            if turn_step == 2:
                turn_step = 3


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

def parse_chess_command(text):
    global show_suggestion, suggested_piece, suggested_move
    text = text.lower().strip()

    # Example: "select a2" or just "a2"
    if text.startswith("select "):
        text = text[7:]  # Remove "select "

    if len(text) == 2:
        file = text[0]
        rank = text[1]

        if file in file_to_index and rank in rank_to_index:
            x = file_to_index[file]
            y = rank_to_index[rank]
            return (x, y)

    return None  # If parsing fails


def record_audio(duration=2.5, filename="command.wav"):
    fs = 44100
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write(filename, fs, recording)
    print("Recording finished.")

def transcribe_audio(filename="command.wav"):
    result = whisper_model.transcribe(filename)
    return result["text"].lower()

def parse_chess_command(command):
    global show_suggestion, suggested_piece, suggested_move,game_over, winner, turn_step
    command = command.strip().lower()
    command = command.rstrip(string.punctuation)
    print("OutsideLoop:", command)

    if command in ["forfeit", "end game"]:
        game_over = True
        if turn_step < 2:
            winner = 'Black wins by forfeit!'
            black_win_sound.play()
        else:
            winner = 'White wins by forfeit!'
            white_win_sound.play()
        print(winner)
        return None

    elif any(word in command for word in ["suggest", "move"]):
        if show_suggestion:
            clear_suggestion()
        else:
            suggest_move()
            show_suggestion = True
        return None

    elif command.startswith("select"):
        command = command.replace("select", "").strip()

    try:
        print(command)
        if len(command) == 2 and command[0] in "abcdefgh" and command[1] in "12345678":
            col = ord(command[0]) - ord('a')
            row = 8 - int(command[1])
            print("Col,Row:", col, row)
            return (col, row)
        else:
            print("Error parsing command")
            error_sound.play();
        return None

    except Exception as e:
        print("Error parsing command:", e)

    return None

def check_options(pieces, locations, turn): #gives all the moves any piece could take
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

def draw_mic_button():
    pygame.draw.rect(screen, (180, 50, 50), mic_button_rect, border_radius=8)
    font = pygame.font.SysFont(None, 24)
    text = font.render('🎙️ Speak', True, (255, 255, 255))
    screen.blit(text, (mic_button_rect.x + 10, mic_button_rect.y + 10))

def handle_click(click_coords):
    global selection, turn_step, valid_moves, winner, game_over, white_options, black_options

    print(click_coords)
    
    if not game_over:
        # White's turn
        if turn_step <= 1:
            # Check for forfeit
            if click_coords == (8, 8) or click_coords == (9, 8):
                winner = 'black'
                black_win_sound.play()
                return

            # If white has already selected a piece and clicks a valid move location
            if selection != 100 and click_coords in valid_moves:
                # Move the piece
                white_locations[selection] = click_coords
                if click_coords in black_locations:
                    black_piece = black_locations.index(click_coords)
                    captured_pieces_white.append(black_pieces[black_piece])
                    if black_pieces[black_piece] == 'king':
                        winner = 'white'
                        white_win_sound.play()
                    black_pieces.pop(black_piece)
                    black_locations.pop(black_piece)
                
                # Update options and change turn
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 2
                print("audio Played")
                black_turn_sound.play()
                selection = 100
                valid_moves = []
                clear_suggestion()
                

            
            # If white clicks on one of their pieces
            elif click_coords in white_locations:
                selection = white_locations.index(click_coords)
                valid_moves = check_valid_moves()
                turn_step = 1
                
        # Black's turn
        elif turn_step > 1:
            # Check for forfeit
            if click_coords == (8, 8) or click_coords == (9, 8):
                winner = 'white'
                white_win_sound.play()
                return

            # If black has already selected a piece and clicks a valid move location
            if selection != 100 and click_coords in valid_moves:
                # Move the piece
                black_locations[selection] = click_coords
                if click_coords in white_locations:
                    white_piece = white_locations.index(click_coords)
                    captured_pieces_black.append(white_pieces[white_piece])
                    if white_pieces[white_piece] == 'king':
                        winner = 'black'
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)
                
                # Update options and change turn
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 0
                print("audio Played")
                white_turn_sound.play()
                selection = 100
                valid_moves = []
                clear_suggestion()
                

            
            # If black clicks on one of their pieces
            elif click_coords in black_locations:
                selection = black_locations.index(click_coords)
                valid_moves = check_valid_moves()
                turn_step = 3
    if not game_over:
        # White's turn
        if turn_step <= 1:
            # Check for forfeit
            if click_coords == (8, 8) or click_coords == (9, 8):
                winner = 'black'
                black_win_sound.play()
                return

            # If white has already selected a piece and clicks a valid move location
            if selection != 100 and click_coords in valid_moves:
                # Move the piece
                white_locations[selection] = click_coords
                if click_coords in black_locations:
                    black_piece = black_locations.index(click_coords)
                    captured_pieces_white.append(black_pieces[black_piece])
                    if black_pieces[black_piece] == 'king':
                        winner = 'white'
                        white_win_sound.play()
                    black_pieces.pop(black_piece)
                    black_locations.pop(black_piece)
                
                # Update options and change turn
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 2
                selection = 100
                valid_moves = []
                clear_suggestion()
            
            # If white clicks on one of their pieces
            elif click_coords in white_locations:
                selection = white_locations.index(click_coords)
                valid_moves = check_valid_moves()
                turn_step = 1
                
        # Black's turn
        elif turn_step > 1:
            # Check for forfeit
            if click_coords == (8, 8) or click_coords == (9, 8):
                winner = 'white'
                white_win_sound.play()
                return

            # If black has already selected a piece and clicks a valid move location
            if selection != 100 and click_coords in valid_moves:
                # Move the piece
                black_locations[selection] = click_coords
                if click_coords in white_locations:
                    white_piece = white_locations.index(click_coords)
                    captured_pieces_black.append(white_pieces[white_piece])
                    if white_pieces[white_piece] == 'king':
                        winner = 'black'
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)
                
                # Update options and change turn
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 0
                selection = 100
                valid_moves = []
                clear_suggestion()
            
            # If black clicks on one of their pieces
            elif click_coords in black_locations:
                selection = black_locations.index(click_coords)
                valid_moves = check_valid_moves()
                turn_step = 3
    print(click_coords)
    if not game_over:
        if turn_step <= 1:
            if click_coords == (8, 8) or click_coords == (9, 8):
                winner = 'black'
                black_win_sound.play()

            # Selecting a white piece
            if click_coords in white_locations:
                selection = white_locations.index(click_coords)
                valid_moves = check_valid_moves()
                if turn_step == 0:
                    turn_step = 1

            # Moving a white piece
            if click_coords in valid_moves and selection != 100:
                white_locations[selection] = click_coords
                if click_coords in black_locations:
                    black_piece = black_locations.index(click_coords)
                    captured_pieces_white.append(black_pieces[black_piece])
                    if black_pieces[black_piece] == 'king':
                        winner = 'white'
                    black_pieces.pop(black_piece)
                    black_locations.pop(black_piece)
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 2
                selection = 100
                valid_moves = []
                clear_suggestion()

        elif turn_step > 1:
            if click_coords == (8, 8) or click_coords == (9, 8):
                winner = 'white'

            # Selecting a black piece
            if click_coords in black_locations:
                selection = black_locations.index(click_coords)
                valid_moves = check_valid_moves() 
                if turn_step == 2:
                    turn_step = 3

            # Moving a black piece
            if click_coords in valid_moves and selection != 100:
                black_locations[selection] = click_coords
                if click_coords in white_locations:
                    white_piece = white_locations.index(click_coords)
                    captured_pieces_black.append(white_pieces[white_piece])
                    if white_pieces[white_piece] == 'king':
                        winner = 'black'
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 0
                selection = 100
                valid_moves = []
                clear_suggestion()



# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    draw_mic_button()
    if selection != 100: #tells we have selected a piece
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if suggestion_button_rect.collidepoint(mouse_pos):
                if show_suggestion:
                    clear_suggestion()  # Turn off and clear highlight
                else:
                    show_suggestion = True
                    suggest_move()

        
        # 🎙️ Mic button clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mic_button_rect.collidepoint(event.pos):
                record_audio()
                spoken_text = transcribe_audio()
                print("Heard:", spoken_text)
                coords = parse_chess_command(spoken_text)  # ✅ Use your parser
                print("Spoken:",coords)
                if coords:
                    handle_click(coords) 

            # 🖱️ Regular board click
            elif not game_over:
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)
                handle_click(click_coords)

        # ⌨️ Press RETURN to restart if game over
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()
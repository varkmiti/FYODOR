import chess
import chess.polyglot
from colored import fg, bg, attr
from tqdm import tqdm
import time

def print_board(board):
    # Define color scheme
    dark_square = bg('grey_30') + fg('white') + attr('bold')
    light_square = bg('white') + fg('black') + attr('bold')

    print("   a   b   c   d   e   f   g   h")
    print(" +--------------------------------+")
    for i in range(8):
        rank = 8 - i
        line = [str(rank)]
        for j in range(8):
            square = chess.square(j, 7 - i)
            piece = board.piece_at(square)
            color = dark_square if (i + j) % 2 == 1 else light_square
            if piece:
                line.append(color + ' ' + str(piece) + ' ' + attr('reset'))
            else:
                line.append(color + ' . ' + attr('reset'))
        print(' '.join(line), '|', str(rank))
    print(" +--------------------------------+")
    print("   a   b   c   d   e   f   g   h")


def move_piece(board, move):
    try:
        move = chess.Move.from_uci(move)
    except:
        print("Invalid move. Please enter a move in UCI format.")
        return False
    if move in board.legal_moves:
        board.push(move)
        return True
    else:
        print("Illegal move.")
        return False
    
def score_bored(board):
    if board.is_checkmate():
        if board.turn:
            return -float('inf')
        else:
            return float('inf')

    score = 0
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
    for (piece, value) in piece_values.items():
        score += len(board.pieces(chess.PIECE_SYMBOLS.index(piece.lower()), chess.WHITE)) * value
        score -= len(board.pieces(chess.PIECE_SYMBOLS.index(piece.lower()), chess.BLACK)) * value

    return score

def minimax(board, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or board.is_game_over():
        return score_bored(board)

    if is_maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, depth):
    best_move = None
    best_score = -float('inf')

    moves = list(board.legal_moves)
    with tqdm(total=len(moves), desc="FYODOR is thinking") as pbar:
        for move in moves:
            board.push(move)
            score = minimax(board, depth-1, -float('inf'), float('inf'), False)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

            pbar.update(1)
            time.sleep(0.01)  # optional, to slow down the bar

    return best_move


def main():
    board = chess.Board()
    player_color = input("Choose your color (w for White, b for Black): ")
    player_color = player_color.lower()

    while not board.is_game_over():
        print("\n")
        print(" ------------------------- ")
        print("   F * Y * O * D * O * R   ")
        print(" ------------------------- ")
        print("\n")
        print(f'Current Score: {score_bored(board)}')
        print_board(board)
        if (board.turn == chess.WHITE and player_color == 'w') or (board.turn == chess.BLACK and player_color == 'b'):
            print("Possible moves:")
            for move in board.legal_moves:
                print(move)
            move = input("Enter your move: ")
            if move == 'q':
                break
            if move_piece(board, move):
                print_board(board)
        else:
            try:
                with chess.polyglot.open_reader("./Human.bin") as reader:
                    main_entry = reader.weighted_choice(board)
                    print("FYODOR recommends: " + str(main_entry.move))
                    board.push(main_entry.move)  # FYODOR makes a move
            except:
                print("No recommended move from opening book. FYODOR will select the best move.")
                move = get_best_move(board, 5)  # added depth parameter
                print("FYODOR recommends: " + str(move))
                board.push(move)

if __name__ == "__main__":
    main()
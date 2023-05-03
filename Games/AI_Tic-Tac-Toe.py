from tkinter import *
import copy
from operator import itemgetter

class TicTacToe:
    winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                            [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    buttons = []

    def __init__(self):
        self.board = [" "] * 9
        self.moves = [StringVar() for _ in range(9)]
        self.x_wins = 0
        self.o_wins = 0
        self.curr_player = "X"
        self.move_number = 0
        self.winning_squares = []
        self.game_over = False

        self.apply_to_each(lambda x: x.set(" "), self.moves)

    def make_move(self, move):
        ai_on.config(state='disabled')
        self.move_number += 1
        if self.curr_player == "X":
            self.board[move] = "X"
            info_text.set("It is O's turn")
            self.curr_player = "O"
            if ai_on_var.get() and self.move_number < 9:
                self.ai_mm_init()
        else:
            self.board[move] = "O"
            info_text.set("It is X's turn")
            self.curr_player = "X"

        if self.game_over:
            return

        self.buttons[move].config(state="disabled")

        winner = self.game_won(self.board)
        if winner is not None:
            self.who_won(winner)
            self.game_over = True

        elif self.move_number == 9 and self.board_full(self.board):
            info_text.set("Draw")
            self.apply_to_each(lambda x: x.config(disabledforeground="red"), self.buttons)
            self.game_over = True

        self.update_board()

    def apply_to_each(self, func, some_list):
        for l in some_list:
            func(l)

    def any_return(self, iterable):
        for e in iterable:
            if e:
                return e
        return False

    def who_won(self, winner):
        if winner == "X":
            info_text.set("X wins!!!")
            self.x_wins += 1
        else:
            info_text.set("O wins!!!")
            self.o_wins += 1

        count_text.set("X: " + str(self.x_wins) + "\tO: " + str(self.o_wins))

        self.apply_to_each(lambda x: x.config(disabledforeground="red"),
                           [self.buttons[s] for s in self.winning_squares])

        for b in self.buttons:
            b.config(state="disabled")

    def reset(self):
        ai_on.config(state='normal')
        self.curr_player = "X"
        self.move_number = 0
        self.game_over = False

        info_text.set("It is X's turn")

        self.board = [" " for _ in self.board]
        self.update_board()

        for b in self.buttons:
            b.config(state="normal")
            b.config(disabledforeground="black")

    def update_board(self):
        for i in range(9):
            self.moves[i].set(self.board[i])

    def game_won(self, gameboard):
        check = self.any_return([self.three_in_a_row(gameboard, c) for c in TicTacToe.winning_combinations])
        if check:
            return check
        else:
            return None

    def three_in_a_row(self, gameboard, squares):
        combo = set(itemgetter(squares[0], squares[1], squares[2])(gameboard))
        if len(combo) == 1 and combo.pop() != " ":
            self.winning_squares = squares
            return gameboard[squares[0]]
        else:
            return None

    def get_enemy(self, curr_player):
        if curr_player == "X":
            return "O"
        else:
            return "X"
            
    def board_full(self, board):
        for s in board:
            if s == " ":
                return False

        return True

    def ai_mm_init(self):
        player = "O"
        a = -1000
        b = 1000

        board_copy = copy.deepcopy(self.board)

        best_outcome = -100

        best_move = None

        for i in range(9):
            if board_copy[i] == " ":
                board_copy[i] = player
                val = self.minimax(self.get_enemy(player), board_copy, a, b)
                board_copy[i] = " "
                if player == "O":
                    if val > best_outcome:
                        best_outcome = val
                        best_move = i
                else:
                    if val < best_outcome:
                        best_outcome = val
                        best_move = i

        self.make_move(best_move)

    def minimax(self, player, board, alpha, beta):
        board_copy = copy.deepcopy(board)

        winner = self.game_won(board_copy)

        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif self.board_full(board_copy):
            return 0

        best_outcome = -100 if player == "O" else 100

        for i in range(9):
            if board_copy[i] == " ":
                board_copy[i] = player
                val = self.minimax(self.get_enemy(player), board_copy, alpha, beta)
                board_copy[i] = " "
                if player == "O":
                    best_outcome = max(best_outcome, val)
                    alpha = min(alpha, best_outcome)
                else:
                    best_outcome = min(best_outcome, val)
                    beta = max(beta, best_outcome)

                if beta <= alpha:
                    return best_outcome

        return best_outcome

root = Tk()
root.title("Tic-Tac-Toe Game")

game = TicTacToe()

welcome_text = StringVar()
welcome_text.set("Welcome to Ian's Tic-Tac-Toe Game!")
welcome = Label(root, textvariable=welcome_text)
welcome.grid(row=0, column=0, columnspan=3)

count_text = StringVar()
count_text.set("X: " + str(game.x_wins) + "\tO: " + str(game.o_wins))
count = Label(root, textvariable=count_text)
count.grid(row=1, column=0, columnspan=3)

info_text = StringVar()
info_text.set("It is X's turn")
info = Label(root, textvariable=info_text)
info.grid(row=2, column=0, columnspan=3)

for square in range(9):
    temp_button = Button(root, textvariable=game.moves[square], command=lambda s=square: game.make_move(s))
    temp_button.grid(row=int((square / 3) + 3), column=(square % 3), sticky=NSEW)
    game.buttons.append(temp_button)

restart_button_text = StringVar()
restart_button_text.set("Restart")
restart_button = Button(root, textvariable=restart_button_text, command=game.reset)
restart_button.grid(row=1, column=0)

ai_on_var = IntVar()
ai_on = Checkbutton(root, text="Turn on AI", variable=ai_on_var)
ai_on.grid(row=1, column=2)

root.columnconfigure(0, minsize=100)
root.columnconfigure(1, minsize=100)
root.columnconfigure(2, minsize=100)
root.rowconfigure(3, minsize=100)
root.rowconfigure(4, minsize=100)
root.rowconfigure(5, minsize=100)

root.mainloop()

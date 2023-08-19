import random
import tkinter as tk
from tkinter import messagebox

class MemoryPuzzleGame:
    def __init__(self):
        self.size = 8  # Size of the board (4x2 grid)
        self.moves = self.size // 2
        self.pairs = []
        self.board = self.create_board()

        self.root = tk.Tk()
        self.root.title("Memory Puzzle Game")
        self.buttons = []

        self.create_widgets()
        self.root.mainloop()

    def create_board(self):
        # Generate a random board with pairs of numbers
        nums = list(range(1, self.moves + 1)) * 2
        random.shuffle(nums)
        board = [nums[i:i + self.size // 2] for i in range(0, self.size, self.size // 2)]
        return board

    def create_widgets(self):
        for i in range(self.size):
            button = tk.Button(self.root, width=6, height=3, command=lambda x=i: self.handle_move(x))
            button.grid(row=i // (self.size // 2), column=i % (self.size // 2))
            self.buttons.append(button)

    def handle_move(self, index):
        if index in self.pairs:
            messagebox.showinfo("Invalid Move", "You've already selected this tile. Try again.")
            return

        row, col = index // (self.size // 2), index % (self.size // 2)
        value = self.make_move(row, col)
        self.pairs.append(index)
        self.buttons[index].config(text=str(value))

        if len(self.pairs) == 2:
            self.root.after(1000, self.check_match)

        if self.check_game_over():
            messagebox.showinfo("Congratulations!", "You've won!")

    def make_move(self, row, col):
        # Update the board with the player's move
        return self.board[row][col]

    def check_match(self):
        move1, move2 = self.pairs[-2:]

        if self.board[move1 // (self.size // 2)][move1 % (self.size // 2)] != self.board[move2 // (self.size // 2)][move2 % (self.size // 2)]:
            self.buttons[move1].config(text="")
            self.buttons[move2].config(text="")

        self.pairs = []
        self.moves -= 1

    def check_game_over(self):
        return self.moves == 0 and len(self.pairs) == 0 and all(button.cget("text") == "" for button in self.buttons)

if __name__ == "__main__":
    game = MemoryPuzzleGame()
    
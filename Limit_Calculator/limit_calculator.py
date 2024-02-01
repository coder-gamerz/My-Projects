import sympy as sp
import tkinter as tk


class Limit_Calculator:
    def __init__(self):
        self.root = tk.Tk()

        self.symbol_text_label = tk.Label(self.root, text='Symbol: ')
        self.symbol_text_label.grid(row=0, column=1, padx=2, pady=2)

        self.symbol_text = tk.Entry(self.root)
        self.symbol_text.grid(row=0, column=2, padx=2, pady=2)

        self.expr_text_label = tk.Label(self.root, text='Expression: ')
        self.expr_text_label.grid(row=1, column=1, padx=2, pady=2)

        self.expr_text = tk.Entry(self.root)
        self.expr_text.grid(row=1, column=2, padx=2, pady=2)

        self.limit_text_label = tk.Label(self.root, text='Limit: ')
        self.limit_text_label.grid(row=3, column=1, padx=2, pady=2)

        self.limit_text = tk.Entry(self.root)
        self.limit_text.grid(row=3, column=2, padx=2, pady=2)
        
        self.limit_calculate = tk.Button(self.root, text='Calculate Limit',command=self.limit_calculator)
        self.limit_calculate.grid(row=4, columnspan=2, column=1,  padx=2, pady=2)

        self.result = tk.Label(self.root, text="")  
        self.result.grid(row=5, columnspan=2, column=1, padx=2, pady=2) 

        tk.mainloop()
        

    def limit_calculator(self):
        self.symbol = sp.symbols(self.symbol_text.get())
        self.expr = self.expr_text.get()
        self.lim = self.limit_text.get()

        self.limit_answer = sp.simplify(sp.limit(self.expr, self.symbol, self.lim))
        self.result.config(text=str(self.limit_answer))
    
Limit_Calculator()

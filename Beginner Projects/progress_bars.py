import math as m
from termcolor import cprint
from colorama import init

init()

def pbar(pr, tot):
    percent = 100 * (pr / float(tot))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    cprint(f"\r[{bar}] {percent:.2f}%", end = "\r", color='red')
    
numbers = [x * 5 for x in range(2000, 3000)]
results = []

pbar(0, len(numbers))
for e, x in enumerate(numbers):
    results.append(m.factorial(x))
    pbar(e + 1, len(numbers))

# A progress bar library to use in programs
    

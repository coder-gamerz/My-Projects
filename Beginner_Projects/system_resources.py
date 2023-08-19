import time
import psutil

def display_usage(cpu, mem, bars=50):
    cpu_percent = (cpu / 100.0)
    cpu_bar = '█' * int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
    mem_percent = (mem / 100.0)
    mem_bar = '█' * int(mem_percent * bars) + '-' * (bars - int(mem_percent * bars)) 
    
    print(f"\rCPU Usage: |{cpu_bar}| {cpu:.2f}%  ", end="")
    print(f"Memory Usage: |{mem_bar}| {mem:.2f}%  ", end="\r")

while True:
    display_usage(psutil.cpu_percent(), psutil.virtual_memory().percent, 30)
    time.sleep(0.5)

# This program shows the CPU and RAM usage of a device.

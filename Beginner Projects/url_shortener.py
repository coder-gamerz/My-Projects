import pyshorteners as p
import clipboard as cp
from customtkinter import * #type: ignore
import time

root = CTk()

def calculate():
    link = str(a.get())
    shawtty = p.Shortener()
    global short_url
    short_url = shawtty.tinyurl.short(link)

    b.configure(text='Your Shortened URL is: \n'+short_url)
    print(short_url)

def copy_url():
    cp.copy(short_url)

a = CTkEntry(root, placeholder_text='Enter URL to shorten')
a.pack()

but = CTkButton(root, text='Shorten', command=calculate)
but.pack()

b = CTkLabel(root, text='')
b.pack()

c = CTkButton(root, text='Copy', command=copy_url)
c.pack()

root.mainloop()

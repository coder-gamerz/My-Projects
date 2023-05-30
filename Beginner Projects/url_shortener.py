import pyshorteners as p
import clipboard as cp
from customtkinter import * #type: ignore

root = CTk()

def calculate():
    link = str(a.get())
    shawtty = p.Shortener()
    short_url = shawtty.tinyurl.short(link)

    b.configure(text='Your Shortened URL is: \n'+short_url)
    cp.copy(short_url)
    c.configure(text='Copied Shortened Link to the Clipboard!')
    print(short_url)

a = CTkEntry(root, placeholder_text='Enter URL to shorten')
a.pack()

but = CTkButton(root, text='Shorten', command=calculate)
but.pack()

b = CTkLabel(root, text='')
b.pack()

c = CTkLabel(root, text='')
c.pack()

root.mainloop()

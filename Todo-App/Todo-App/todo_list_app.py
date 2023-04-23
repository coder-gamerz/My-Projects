from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import Database

db = Database('store.db')
def populate_todo_list():
    todo_list.delete(0, END)
    for item in db.fetch():
        todo_list.insert(END, [item[0], item[1], item[2], item[3]])
    return todo_list.get(0, END)

def add_todo_item(*args):
    if todo_text.get() == '':
        messagebox.showerror('Require Input', 'Todo entry is required')
        return

    db.insert(todo_text.get())
    todo_list.insert(END, (todo_text.get()))
    populate_todo_list()
    clear_box()
    todo_list.see(END)

def delete_todo_item():
    try:
        index_item = todo_list.curselection()[0]
        selected_item = todo_list.get(index_item)
        db.delete(selected_item[0])
        populate_todo_list()
        clear_box()
    except IndexError:
        messagebox.showerror('Delete error', 'Select item for deleting')

def update_todo_item():
    try:
        index_item = todo_list.curselection()[0]
        selected_item = todo_list.get(index_item)
        db.update(selected_item[0], todo_text.get())
        populate_todo_list()
        clear_box()
    except IndexError:
        messagebox.showerror('Update error', 'Select item for updating')

def select_item(*args):
    index_item = todo_list.curselection()[0]
    selected_item = todo_list.get(index_item)
    todo_text.set(selected_item[1])
    created_at_var.set(selected_item[2].strftime("%b %d %Y"))
    updated_at_var.set(selected_item[3].strftime("%b %d %Y"))
    print(index_item)

def clear_box():
    todo_entry.delete(0, END)

app = Tk()
style = ttk.Style()
mainframe = ttk.Frame(app, padding=(3,3,12,12))
mainframe.grid(column=0, row=0)
todo_title = Label(mainframe, text='Todo App', font=('bold', 16))
todo_title.grid(column=0, row=0, sticky=(W, E), columnspan=3, pady=10)
todo_text = StringVar()
todo_lbl = ttk.Label(mainframe, text='Your Entry')
todo_lbl.grid(column=0, row=1, sticky=W)
todo_entry = ttk.Entry(mainframe, textvariable=todo_text, width=50)
todo_entry.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=(W, E))
add_btn = ttk.Button(mainframe, text='Add', command=add_todo_item)
add_btn.grid(column=2, row=1, sticky=E, ipadx=4, ipady=4)
created_at_lbl = ttk.Label(mainframe, text='Created at:')
created_at_lbl.grid(column=1, row=2, sticky=W, ipady=5, ipadx=5, padx=5, pady=5)
created_at_lbl = ttk.Label(mainframe, text='Updated at:')
created_at_lbl.grid(column=1, row=2, sticky=E, ipady=5, ipadx=5, padx=68, pady=5)
created_at_var = StringVar()
created_at_date = ttk.Label(mainframe, textvariable=created_at_var)
created_at_date.grid(column=1, row=2, sticky=W, padx=68)
updated_at_var = StringVar()
updated_at_date = ttk.Label(mainframe, textvariable=updated_at_var)
updated_at_date.grid(column=1, row=2, sticky=E, padx=5)
list_text = StringVar()
todo_list = Listbox(mainframe, width=70, height=10, border=0)
todo_list.grid(column=1, row=3, sticky=(W,E), ipady=5, ipadx=5, padx=5, pady=5)
del_btn = ttk.Button(mainframe, text='Delete Item', command=delete_todo_item)
del_btn.grid(column=1, row=4, sticky=W, ipady=5, ipadx=5, padx=5, pady=5)
clr_btn = ttk.Button(mainframe, text='Clear Input', command=clear_box)
clr_btn.grid(column=1, row=4, sticky=NS, ipady=5, ipadx=5, padx=5, pady=5)
update_btn = ttk.Button(mainframe, text='Update Item', command=update_todo_item)
update_btn.grid(column=1, row=4, sticky=E, ipady=5, ipadx=5, padx=5, pady=5)
scrlbr = ttk.Scrollbar(mainframe, orient=VERTICAL, command=todo_list.yview)
scrlbr.grid(column=2, row=3, sticky=W)
todo_list.configure(yscrollcommand=scrlbr.set, height=12)
todo_list.bind('<<ListboxSelect>>', select_item)
app.bind('<Return>', add_todo_item)
populate_todo_list()

for item in range(0, len(populate_todo_list()), 2):
    todo_list.itemconfigure(item, background='#ccc')
    
app.title("Todo App")
app.geometry('600x400')
app.mainloop()
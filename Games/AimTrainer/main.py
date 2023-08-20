from tkinter import *
import random,time


application = Tk()
application.minsize(height=500, width=550)
application.configure(bg='black')
application.title("Clicker Game")


timerStart = time.time()
def startGame():
    display.delete(ALL)
    target = display.create_rectangle(250, 250, 225, 225, fill="red", outline="maroon", width=2)
    display.tag_bind(target, "<Button-1>", figureClicked)
    global timerStart
    timerStart = time.time()


points = 0
def figureClicked(self):
    global points
    display.delete(ALL)
    new_x = random.randint(0, 475)
    new_y = random.randint(0, 475)
    target = display.create_rectangle(0, 0, 25, 25, fill="red", outline="maroon", width=2)
    display.tag_bind(target, "<Button-1>", figureClicked)
    display.coords(target, new_x, new_y, new_x + 25, new_y + 25)
    global timerStart
    if time.time() - timerStart <= 2:
        points += 1
        scoreLabel.config(text="High Score : " + str(points))
    timerStart = time.time()



button1 = Button(application, text="START", bg="lightblue", command = startGame)
button1.pack()
display = Canvas(application, width=500, height=500, bg="lightgreen", cursor="cross")
display.pack()
scoreLabel = Label(application, text="High Score : 0", bg="lightblue",relief="sunken")
scoreLabel.pack()
application.mainloop()

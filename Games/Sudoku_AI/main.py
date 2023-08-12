import pygame, sys, random, time
from pygame.locals import *

top = -1
MyStack = []
FPS = 60
WINDOWWIDTH = 720
WINDOWHEIGHT = 540
BOXSIZE = 50
GAPSIZE = 10
MINIGAPSIZE = 5

HINTSPEED = 8
BOARDWIDTH = 9
BOARDHEIGHT = 9

HINTS = 5
LIVES = 5
SCOREBOARD = 100


XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE+MINIGAPSIZE) + 2 * GAPSIZE))/2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE+MINIGAPSIZE) + 2 * GAPSIZE))/2)

WINDOWHEIGHT = WINDOWHEIGHT + SCOREBOARD

assert (BOARDWIDTH * BOARDHEIGHT == 81), 'Board needs to have 81 boxes.'

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0 ,255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255,128, 0)
PURPLE = (255,0,255)
CYAN = (0,255,255)
BLACK = (0, 0, 0)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

TEXTCOLOR = BLACK
BASICFONTSIZE = 20



		
		





#SUDOKU = [[4,2,7,3,1,9,0,0,8],[0,0,0,0,8,0,0,0,0],[0,8,0,4,0,2,0,0,0],[1,3,0,0,7,0,0,6,5],[0,0,4,0,0,5,0,2,9],[0,0,8,2,6,1,3,0,0],[8,7,1,5,0,0,0,0,0],[0,0,6,0,9,8,7,0,3],[3,4,0,6,2,0,0,0,0]]
#PLAYERSUDOKU = [[4,2,7,3,1,9,0,0,8],[0,0,0,0,8,0,0,0,0],[0,8,0,4,0,2,0,0,0],[1,3,0,0,7,0,0,6,5],[0,0,4,0,0,5,0,2,9],[0,0,8,2,6,1,3,0,0],[8,7,1,5,0,0,0,0,0],[0,0,6,0,9,8,7,0,3],[3,4,0,6,2,0,0,0,0]]

def main():
	global FPSCLOCK, DISPLAYSURF,BASICFONT,MSG_SURF, MSG_RECT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, MSG, top, MyStack

	SOLVE_CHECK = 0 
	RESET_CHECK = 0 
	NEWGAME_CHECK = 0
	generate()
	pygame.init()
	pygame.mixer.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption("SUDOKU")
	BASICFONT = pygame.font.Font('freesansbold.ttf',BASICFONTSIZE)
	RESET_SURF, RESET_RECT = makeText('Reset ', TEXTCOLOR, RED, WINDOWWIDTH-120, WINDOWHEIGHT-90)
	NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, BOXCOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-60)
	SOLVE_SURF, SOLVE_RECT = makeText('Solve ', TEXTCOLOR, GREEN, WINDOWWIDTH-120, WINDOWHEIGHT-30)
		
	mousex = 0
	mousey = 0
	firstSelection = None
	DISPLAYSURF.fill(BGCOLOR)
	
	while True:
		MSG = False
		DISPLAYSURF.fill(BGCOLOR)
		drawBoard()
		if SOLVE_CHECK == 1:
			SOLVE_SURF, SOLVE_RECT = makeText('Solve ', TEXTCOLOR, GREEN, WINDOWWIDTH-120, WINDOWHEIGHT-30)
		if NEWGAME_CHECK == 1:
			NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, BOXCOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-60)
		if RESET_CHECK ==	 1:
			RESET_SURF, RESET_RECT = makeText('Reset ', TEXTCOLOR, RED, WINDOWWIDTH-120, WINDOWHEIGHT-90)
		for event in pygame.event.get():
			if event.type == QUIT or (event.type==KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex,mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex,mousey = event.pos
				boxx, boxy = getBoxAtPixel(mousex, mousey)
				if (boxx, boxy) == (None, None):
					if SOLVE_RECT.collidepoint(mousex, mousey):
						top = -1
						MyStack = []
						reset()
						MSG = True
						MSG_SURF, MSG_RECT = makeText('Solving Please Wait!!!', TEXTCOLOR, BGCOLOR, WINDOWWIDTH//2-100, WINDOWHEIGHT-30)	
						solve()

					elif RESET_RECT.collidepoint(mousex, mousey):
						top = -1
						MyStack = []
						reset()
						

						
					elif NEW_RECT.collidepoint(mousex, mousey):
						top = -1
						MyStack = []
						generate()
						

					

			elif (event.type == KEYUP):
				if event.key>=49 and event.key<=57:
					playerSolve(mousex,mousey,int(event.key)-48)
				elif event.key == K_BACKSPACE:
					clearNumber(mousex, mousey)
	




			


			
				
		boxx, boxy = getBoxAtPixel(mousex,mousey)
		if boxx!=None and boxy!=None:
			drawHighlightBox(boxx,boxy)
		elif boxx==None and boxy == None:
			if SOLVE_RECT.collidepoint(mousex, mousey):
				SOLVE_SURF, SOLVE_RECT = makeText('Solve ', GREEN, TEXTCOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-30)
				SOLVE_CHECK = 1
			elif RESET_RECT.collidepoint(mousex, mousey):
				RESET_SURF, RESET_RECT = makeText('Reset ', RED, TEXTCOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-90)
				RESET_CHECK = 1
			elif NEW_RECT.collidepoint(mousex, mousey):
				NEW_SURF, NEW_RECT = makeText('New Game', BOXCOLOR, TEXTCOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-60)
				NEWGAME_CHECK = 1


		

	
			
		pygame.display.update()
		FPSCLOCK.tick(FPS)


def generate():
	CLUES = 12
	global SUDOKU, PLAYERSUDOKU, top, MyStack
	SUDOKU = []
	PLAYERSUDOKU = []
	usedIndices = []			
	for i in range(9):
		new = []
		newVariable = []
		for j in range(9):
			new.append(0)
			newVariable.append(0)
		SUDOKU.append(new)
		PLAYERSUDOKU.append(newVariable)	
	i = 1   #Second Row

	while(CLUES):
		ROUND = 4      #Randomly generate 4 numbers in each loop
		while(ROUND):
			j = random.randint(0,8)
			if (i,j) not in usedIndices:
				number = random.randint(1,9)
				if (isValidSudoku(i,j,number)):
					usedIndices.append((i,j))
					CLUES-=1
					ROUND-=1
					PLAYERSUDOKU[i][j] = number
					SUDOKU[i][j] = number
		i+=3    #Incrementing row from 2 to 5 and then 5 to 8.
	if checkGeneratedSudoku():    #Solving the generated puzzle 
		top = -1				  #if it returns then sudoku is solvable
		MyStack = []
		A = checkGeneratedSudoku()
	else:
		top = -1
		MyStack = []
		generate()
	PLAYERSUDOKU= []
	SUDOKU = []
	for i in range(9):
		new = []
		newVariable = []
		for j in range(9):
			new.append(0)
			newVariable.append(0)
		PLAYERSUDOKU.append(new)
		SUDOKU.append(newVariable)
	CLUES = 30
	usedIndices = []
	while(CLUES):
		i = random.randint(0,8)
		j = random.randint(0,8)
		

		if ((i, j)) not in usedIndices:
			CLUES-=1
			PLAYERSUDOKU[i][j] = A[i][j]
			SUDOKU[i][j] = A[i][j]
			usedIndices.append((i, j))


def playerSolve(x, y, number):
	if number>0 and number<=9:
		boxx, boxy = getBoxAtPixel(x, y)
		if boxx!=None and boxy!=None and SUDOKU[boxy][boxx]==0:
			if isValidSudoku(boxy, boxx, number):

				PLAYERSUDOKU[boxy][boxx] = number
				left, top = leftTopCoordsOfBox(boxx,boxy)
				pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
				textSurf = BASICFONT.render(str(PLAYERSUDOKU[boxy][boxx]), True, TEXTCOLOR)
				textRect = textSurf.get_rect()
				textRect.center = int(left + BOXSIZE/2),int(top+BOXSIZE/2)
				DISPLAYSURF.blit(textSurf, textRect)
			elif not isValidSudoku(boxy, boxx, number):
				pygame.mixer.music.load(r'wrongMove.mp3')
				pygame.mixer.music.play()
				pygame.event.wait()
def clearNumber(x, y):

	boxx, boxy = getBoxAtPixel(x, y)
	if boxx!=None and boxy!=None:
		PLAYERSUDOKU[boxy][boxx] = 0
			
				

def isValidSudoku(x, y, number):
	global PLAYERSUDOKU

	i = x
	for j in range(9):
		if(PLAYERSUDOKU[i][j] == number):

			return False
   
	j = y
	for i in range(9):
		if(PLAYERSUDOKU[i][j] == number):
			return False
	counter1 = int(x/3)*3   #counter1 can take values 0,1,2
	counter2 = int(y/3)*3 #As counter1
	for i in range(counter1,counter1+3):
		for j in range(counter2,counter2+3):
			if (PLAYERSUDOKU[i][j] == number):
				return False
            

	return True




def leftTopCoordsOfBox(boxx, boxy):

	counter1 = int(boxx/3)
	counter2 = int(boxy/3)

	left = (boxx*(BOXSIZE+MINIGAPSIZE))+(counter1 * GAPSIZE)+XMARGIN
	top = (boxy*(BOXSIZE+MINIGAPSIZE))+(counter2*GAPSIZE)+YMARGIN
	return (left, top)

def drawBoard():
	global PLAYERSUDOKU
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left, top = leftTopCoordsOfBox(boxx,boxy)
			pygame.draw.rect(DISPLAYSURF, GRAY, (left, top, BOXSIZE, BOXSIZE))
			if(PLAYERSUDOKU[boxy][boxx]!=0):
				textSurf = BASICFONT.render(str(PLAYERSUDOKU[boxy][boxx]), True, TEXTCOLOR)
				textRect = textSurf.get_rect()
				textRect.center = int(left + BOXSIZE/2),int(top+BOXSIZE/2)
				DISPLAYSURF.blit(textSurf, textRect)
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			if(SUDOKU[boxy][boxx]!=0):
				left, top = leftTopCoordsOfBox(boxx,boxy)
				pygame.draw.rect(DISPLAYSURF, GRAY, (left, top, BOXSIZE, BOXSIZE))
				textSurf = BASICFONT.render(str(SUDOKU[boxy][boxx]), True, WHITE, GRAY)
				textRect = textSurf.get_rect()
				textRect.center = int(left + BOXSIZE/2),int(top+BOXSIZE/2)
				DISPLAYSURF.blit(textSurf, textRect)




	DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
	DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
	DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
	
	
	if MSG:
		DISPLAYSURF.blit(MSG_SURF, MSG_RECT)


def getBoxAtPixel(x, y):
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left, top = leftTopCoordsOfBox(boxx,boxy)
			boxRect = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
			if boxRect.collidepoint(x, y):
				return (boxx,boxy)
	return (None,None)

def drawHighlightBox(boxx, boxy):
	left, top = leftTopCoordsOfBox(boxx, boxy)
	pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left-5, top-5, BOXSIZE+10, BOXSIZE+10), 4)

def makeText(text, color, bgcolor, top, left):
	textSurf = BASICFONT.render(text, True, color, bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (top, left)
	return (textSurf, textRect)

def solve():
	global PLAYERSUDOKU, SUDOKU
	
	
	i=0
	j=0
	data = 1
	while(i<9):

		if PLAYERSUDOKU[i][j] != 0:
			
			if j<8:
				j+=1
			else:
				j=0
				i+=1
			
		elif isValidSudoku(i,j,data):
			
			PLAYERSUDOKU[i][j] = data
			push(i, j, data)
			data = 1
			if j<8:
				j+=1
			else:
				j=0
				i+=1
			
		elif data<9:
			data+=1
			
		elif (not stackIsEmpty()):
			i = give_row()
			j = give_column()
			data = give_data()
			pop()
			PLAYERSUDOKU[i][j] = 0
			run = True
			while run:
				if data<9:
					data+=1
					run = False
				else:
					i = give_row()
					j = give_column()
					data = give_data()
					pop()
					PLAYERSUDOKU[i][j] = 0


		drawBoard()
		pygame.display.update()
		FPSCLOCK.tick(2000)

def checkGeneratedSudoku():
	
	global PLAYERSUDOKU
		
	i=0
	j=0
	data = 1
	while(i<9):

		if PLAYERSUDOKU[i][j] != 0:
			
			if j<8:
				j+=1
			else:
				j=0
				i+=1
			
		elif isValidSudoku(i,j,data):
				
			PLAYERSUDOKU[i][j] = data
			push(i, j, data)
			data = 1
			if j<8:
				j+=1
			else:
				j=0
				i+=1
				
		elif data<9:
			data+=1
			
		elif (not stackIsEmpty()):
			i = give_row()
			j = give_column()
			data = give_data()
			pop()
			PLAYERSUDOKU[i][j] = 0
			run = True
			while run:
				if data<9:
					data+=1
					run = False
				else:
					i = give_row()
					j = give_column()
					data = give_data()
					
					pop()
					
					PLAYERSUDOKU[i][j] = 0
		else:
			return False

	
	return PLAYERSUDOKU

		



def push(i, j, data):
	global top, MyStack
	top+=1
	MyStack.append([i,j,data])

def pop():
	global top,MyStack
	top-=1
	MyStack.pop()

def give_row():
	global top, MyStack
	row=MyStack[top][0]
	return row

def give_column():
	global top, MyStack
	column = MyStack[top][1]
	return column

def give_data():
	global top, MyStack
	data = MyStack[top][2]
	return data

def stackIsEmpty():
	global top
	if top==-1:
		return True
	return False

def reset():
	global PLAYERSUDOKU
	for i in range(9):
		for j in range(9):
			PLAYERSUDOKU[i][j]=SUDOKU[i][j]

if __name__ == '__main__':
	main()
	

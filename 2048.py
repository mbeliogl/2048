
import pygame,numpy,random,sys
from pygame.locals import *

Size = 4                                          
Block_WH = 110                                   
BLock_Space = 10                                  
Block_Size = Block_WH*Size+(Size+1)*BLock_Space
# using numpy to create an array that represents the board. 4 columns and four rows #
Board = numpy.zeros([Size,Size])                 
Screen_Size = (Block_Size,Block_Size+110)
Title_Rect = pygame.Rect(0,0,Block_Size,110)     

Score = 0
# setting rgb values for different blocks as well as some screen and block sizes (will be used later).
BlockColor = {
	0:(255,255,255),
	2:(230,170,170),
	4:(100,200,200),
	8:(255,255,0),
	16:(0,255,150),
	32:(0,100,255),
	64:(100,149,237),
	128:(72,61,139),
	256:(106,90,205),
	512:(123,104,238),
	1024:(65,105,225),
	2048:(0,0,255),
	4096:(30,144,255),
}                                          

class Game():	
	
	def __init__(self,board):
			self.board = board
			self.score  = 0
			self.zerolist = []
	# adds the two numbers if they could be added (if they are equal) on the left. One at a time. 
	def addList(self,rowlist):
			
			startnum = 0
			endnum = Size-rowlist.count(0)-1
			#if the left number is equal to the right number
			while startnum < endnum:
					if rowlist[startnum] == rowlist[startnum+1]:
						#multiply the left number by 2
						rowlist[startnum] *= 2
						rowlist[startnum+1:] = rowlist[startnum+2:]
						rowlist.append(0)
						#update the score 
						self.score += int(rowlist[startnum])         
					startnum += 1
			return rowlist

	#for example: makes a list [2,0,4,0] into [2,4,0,0] 
	def removeZero(self,rowlist):
			
			while True:
					copy = rowlist[:]     
					
					try:
						rowlist.remove(0)
						rowlist.append(0)
					
					except:
						pass
					#if the number is already on the very left
					if rowlist == copy:
						break
			#returns the list after the move 
			return self.addList(rowlist)

	# updates the board
	def update(self,board):
			#makes a copy of the 0 board
			lastboard = board.copy()
			#gets number of rows and number of columns using shape() method
			m,n = board.shape
			
			for i in range(m):
					newList = self.removeZero(list(board[i])) #making every row in the board a list. Removes zeroes by calling removeZero() for each row
					#change the board to new board
					board[i] = newList
					#for each number in a row, from the rightmost to the rightmost non-zero
					for k in range(Size-1,Size-newList.count(0)-1,-1):     
						self.zerolist.append((i,k))
			#if the board can be left moved, execute the line and generate a number; if not, the line wont be execute and the random number wont be generated
			if board.min() == 0 and (board!=lastboard).any():       
					setGame.Generate(Size,board,self.zerolist)
			return board

# initates the move classes that define how the board should behave with every move
class LeftAction(Game):
	#inherits the board from the game class
	def __init__(self,board):
		super(LeftAction, self).__init__(board)
	# makes a copy of the board and calls the update method on it. returns the new board and the current score
	def get(self):
		board = self.board.copy()                               
		newboard = self.update(board)
		return newboard,self.score
#same thing
class RightAction(Game):
	def __init__(self,board):
		super(RightAction, self).__init__(board)

	def get(self):
		board = self.board.copy()[:,::-1]
		newboard = self.update(board)
		return newboard[:,::-1],self.score
#same thing
class UpAction(Game):
	def __init__(self,board):
		super(UpAction, self).__init__(board)

	def get(self):
		board = self.board.copy().T
		newboard = self.update(board)
		return newboard.T,self.score

#same thing
class DownAction(Game):
	def __init__(self,board):
		super(DownAction, self).__init__(board)

	def get(self):
		board = self.board.copy()[::-1].T
		newboard = self.update(board)
		return newboard.T[::-1],self.score


class setGame():
	def __init__(self,board):
		self.board = board

	# gets the positons of all 0's (which serve as empty spaces) from the zerolist
	def getRandomZero(zerolist = []):
		if zerolist == []:
			a = random.randint(0,Size-1)
			b = random.randint(0,Size-1)
		# if zeroList already contains some tuples, choose a random tuple
		else:
			a,b = random.sample(zerolist,1)[0]
		return a,b

	# generate a random 2 or 4 using random
	def getTwos():         
		n = random.random()
		if n > 0.8:
				n = 4
		else:
			n = 2
		return n

	# places a random 2 or 4 into the position from getPosition()
	@classmethod
	def Generate(self,Size,board = None,zerolist = []): 
		if numpy.all(board == None):
			board = Board.copy()
			
		a,b = self.getRandomZero(zerolist)    
		n = self.getTwos()
		board[a][b] = n
		#return the new board
		return board  

	
	@classmethod
	def drawSurface(self,screen,board,score):
		#pygame generates a rectangle of the title 
		pygame.draw.rect(screen,(255,255,255),Title_Rect)   
		#deternimes the font of the letters and numbers
		font1 = pygame.font.SysFont('arial',48)
		#allows to draw one object on the other using blit()
		screen.blit(font1.render('Score:',True,(0,170,0)),(140,25))     
		screen.blit(font1.render(str(score),True,(0,170,0)),(285,27))
		#nested for loop to draw the blit()
		a,b = board.shape
		for i in range(a):
			for j in range(b):
				self.drawBlock(screen,i,j,BlockColor[board[i][j]],board[i][j])

	# Display 'Game Over' message when the game is over
	@classmethod
	def drawGameOver(self, screen, score):
		pygame.draw.rect(screen,(255,255,255),Title_Rect)
		font1 = pygame.font.SysFont('arial',48)
		font2 = pygame.font.SysFont('arial',20)
		screen.blit(font1.render('GAME OVER!',True,(0,170,0)),(120,25))
		screen.blit(font2.render('Final Score:',True,(0,170,0)),(185,80))
		screen.blit(font2.render(str(score),True,(0,170,0)),(285,80))



	# pygame is used to draw the smaller blocks (ones that move)
	def drawBlock(screen,row,column,color,blocknum):
		font = pygame.font.SysFont('stxingkai',80)
		#sets width of the blocks and their height
		w = column*Block_WH+(column+1)*BLock_Space
		h = row*Block_WH+(row+1)*BLock_Space+110
		pygame.draw.rect(screen,color,(w,h,110,110))
		# if the block is not blank then you draw it.
		if blocknum != 0:
			fw,fh = font.size(str(int(blocknum)))
			screen.blit(font.render(str(int(blocknum)),True,(0,0,0)),(w+(110-fw)/2,h+(110-fh)/2))

	# defines what button was pressed (arrow keys) 
	def keyDownPressed(keyvalue,board):
		if keyvalue == K_LEFT:
			return LeftAction(board)
		elif keyvalue == K_RIGHT:
			return RightAction(board)
		elif keyvalue == K_UP:
			return UpAction(board)
		elif keyvalue == K_DOWN:
			return DownAction(board)

	# Decide if the game is over or not 
	def gameOver(board):
		testboard = board.copy()
		#gets the 4 by 4
		a,b = testboard.shape
			
		for i in range(a):
			for j in range(b-1):
				#check if there are adjacent numbers that are equal(could be added together)
				if testboard[i][j] == testboard[i][j+1]:    
					#game not over
					return False
			# same for columns
		for i in range(b):
			for j in range(a-1):
				if testboard[j][i] == testboard[j+1][i]:
					return False
		print('GAME OVER')
		return True

def main():
	pygame.init()
	#sets up the screen
	screen = pygame.display.set_mode(Screen_Size,0,32)
	pygame.display.set_caption('2048')  
	# gets the board using the Generate() method
	board = setGame.Generate(Size)
	#cuurenscore starts with 0 (accumulator)
	currentscore = 0
	# uses drawSurface() to draw the rectangle
	setGame.drawSurface(screen,board,currentscore)
	#updates the screen after the move
	pygame.display.update()
  
	while True:
		# for every event determine if it is quit (exit) and act accordingly
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)
			# if not, judge the user action and move the board accordingly
			elif event.type == pygame.KEYDOWN:
				#assignes variable to action
				action = setGame.keyDownPressed(event.key,board)    
				board,score = action.get()   
				#updates the score
				currentscore += score   
				setGame.drawSurface(screen,board,currentscore)
				# if there are no zeros in the board, check if the game is over using gameOver()
				if board.min() != 0:
					over = setGame.gameOver(board)
					if over:
						setGame.drawGameOver(screen, currentscore)
									
		#update after each move
		pygame.display.update()

main()



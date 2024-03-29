#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# NOTE FOR WINDOWS USERS:
# You can download a "exefied" version of this game at:
# http://hi-im.laria.me/progs/tetris_py_exefied.zip
# If a DLL is missing or something like this, write an E-Mail (me@laria.me)
# or leave a comment on this gist.

# Very simple tetris implementation
# 
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# Copyright (c) 2010 "Laria Carolin Chabowski"<me@laria.me>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random
import time
import pygame, sys

# The configuration
cell_size =	18
cols =		10
rows =		22
maxfps = 	30


colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) # Helper color for background grid
]

# Define the shapes of the single parts
tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 2, 2],
	 [2, 2, 0]],
	
	[[3, 3, 0],
	 [0, 3, 3]],
	
	[[4, 0, 0],
	 [4, 4, 4]],
	
	[[0, 0, 5],
	 [5, 5, 5]],
	
	[[6, 6, 6, 6]],
	
	[[7, 7],
	 [7, 7]]
]

def rotate_clockwise(shape):
	return [ [ shape[y][x]
			for y in range(len(shape)) ]
		for x in range(len(shape[0]) - 1, -1, -1) ]

def check_collision(boardX, shape, offset):
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			try:
				if cell and boardX[ cy + off_y ][ cx + off_x ]:
					return True
			except IndexError:
				return True
	return False

def remove_row(boardX, row):
	#print('Holy shit we cleared a line!')
	del boardX[row]
	return [[0 for i in range(cols)]] + boardX
	
def join_matrixes(mat1, mat2, mat2_off):
	off_x, off_y = mat2_off
	for cy, row in enumerate(mat2):
		for cx, val in enumerate(row):
			mat1[cy+off_y-1	][cx+off_x] += val
	return mat1

def new_board():
	boardX = [ [ 0 for x in range(cols) ]
			for y in range(rows) ]
	boardX += [[ 1 for x in range(cols)]]
	return boardX

def check_move(boardY, shape, next_shape):
	stone = [row[:] for row in shape]
	next_stone = [row[:] for row in next_shape]
	testBoard = [row[:] for row in boardY]
	if stone == [[7,7],[7,7]]:
		rotations = 1
	elif stone == [[6,6,6,6]] or stone == [[0,2,2],[2,2,0]] or stone == [[3,3,0],[0,3,3]]:
		rotations = 2
	else:
		rotations = 4
	if next_stone == [[7,7],[7,7]]:
		next_rotations = 1
	elif next_stone == [[6,6,6,6]] or next_stone == [[0,2,2],[2,2,0]] or next_stone == [[3,3,0],[0,3,3]]:
		next_rotations = 2
	else:
		next_rotations = 4
	

	alpha = [[0,0],[999999999999,-10,10000]] #[[number of rotations, number of moves right], number of empty squares]
	beta = [[0,0],[0,0,0]]
	for x in range(rotations):
		stone = rotate_clockwise(stone)
		for y in range(11-len(stone[0])): #number of places the stone can move right
			stone_xx = y
			stone_yy = 0
			while(check_collision(testBoard, stone, (stone_xx, stone_yy)) == False):
			      stone_yy += 1
			testBoard = join_matrixes(testBoard, stone, (stone_xx, stone_yy))
			clearedLines = 0
			for z in range(len(testBoard)-1):
				lineClear = True
				for w in range(len(testBoard[z])):
					if testBoard[z][w] == 0:
						lineClear = False
				if lineClear == True:
					clearedLines += 1
					del testBoard[z]
					testBoard = [[0 for i in range(cols)]] + testBoard
					
			testBoard2 = [row[:] for row in testBoard]
			for s in range(next_rotations):
				next_stone = rotate_clockwise(next_stone)
				for t in range(11-len(next_stone[0])):
					#print('start looking 2 ply x places')
					next_stone_xx = t
					next_stone_yy = 0
					#print('testBoard\n',testBoard)
					while(check_collision(testBoard, next_stone, (next_stone_xx, next_stone_yy)) == False):
						next_stone_yy +=1
						#print('no collision')
					#print('found collision point',next_stone_yy)
					testBoard = join_matrixes(testBoard, next_stone, (next_stone_xx, next_stone_yy))
					#print('placed the second stone\n',testBoard)

					for z in range(len(testBoard)-1):
						lineClear = True
						for w in range(len(testBoard[z])):
							if testBoard[z][w] == 0:
								lineClear = False
						if lineClear == True:
							clearedLines += 1
							del testBoard[z]
							testBoard = [[0 for i in range(cols)]] + testBoard

					allZeros = True
					while allZeros == True:
						for z in range(len(testBoard[0])):
							if testBoard[0][z] != 0:
								allZeros = False
						if allZeros == True:
							del testBoard[0]

					gapHoles = 0
					for z in range(10):
						columnCapped = False
						testY = 0
						while testY < len(testBoard):
							if testBoard[testY][z] != 0:
								columnCapped = True
							if columnCapped == True and testBoard[testY][z] == 0:
								gapHoles += 1
							testY += 1

					n = 1000000000000000
					negativeScore = 0
					for a in range(len(testBoard)-1):
						for b in range(len(testBoard[a])):
							       if testBoard[len(testBoard)-2-a][b] == 0:
								       negativeScore += n
								       #print(beta, negativeScore)
						n = n/10

					beta = [[x+1,y,s+1,t],[negativeScore, clearedLines, gapHoles]]#[[rotations,moves right, rotations2, movesright2],[negativeScore, linesCleared]]
					priorityTwo = 0
					priorityThree = 0
					if len(testBoard) < 18:
						priorityTwo = 2
						priorityThree = 0
					else:
						priorityTwo = 0
						priorityThree = 2
					if beta[1][1] > alpha[1][1]:
						alpha = [row[:] for row in beta]
						#print(testBoard)
					elif beta[1][1] == alpha[1][1]:
						if beta[1][priorityTwo] < alpha[1][priorityTwo]:
							alpha = [row[:] for row in beta]
						elif beta[1][priorityTwo] == alpha[1][priorityTwo]:
							if beta[1][priorityThree] < alpha[1][priorityThree]:
								alpha = [row[:] for row in beta]
							#print('alpha',alpha)
					#print('BoardY\n',boardY)
					testBoard = [row[:] for row in testBoard2] #set testBoard back equal to the original board
					#print('testBoard\n',testBoard)
					#quit()#added this quit line, so I could look at the print methods after one itteration of the nested loops
			testBoard = [row[:] for row in boardY]
	#print('we made |a decision')
	return alpha[0]

class TetrisApp(object):
	def __init__(self):
		pygame.init()
		pygame.key.set_repeat(250,25)
		self.width = cell_size*(cols+6)
		self.height = cell_size*rows
		self.rlim = cell_size*cols
		self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(cols)] for y in range(rows)]
		
		self.default_font =  pygame.font.Font(
			pygame.font.get_default_font(), 12)
		
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
							     # mouse movement
							     # events, so we
							     # block them.
		self.next_stone = tetris_shapes[random.randint(0,len(tetris_shapes)-1)]
		#self.next_stone = tetris_shapes[5]
		self.init_game()
	
	def new_stone(self):
		self.stone = self.next_stone[:]
		self.next_stone = tetris_shapes[random.randint(0,len(tetris_shapes)-1)]
		#self.next_stone = tetris_shapes[5]
		self.stone_x = int(cols / 2 - len(self.stone[0])/2)
		self.stone_y = 0
		
		if check_collision(self.board,
				   self.stone,
				   (self.stone_x, self.stone_y)):
			self.gameover = True
	
	def init_game(self):
		self.board = new_board()
		self.new_stone()
		self.level = 1
		self.score = 0
		self.lines = 0
		pygame.time.set_timer(pygame.USEREVENT+1, 1000)
	
	def disp_msg(self, msg, topleft):
		x,y = topleft
		for line in msg.splitlines():
			self.screen.blit(
				self.default_font.render(
					line,
					False,
					(255,255,255),
					(0,0,0)),
				(x,y))
			y+=14
	
	def center_msg(self, msg):
		for i, line in enumerate(msg.splitlines()):
			msg_image =  self.default_font.render(line, False,
				(255,255,255), (0,0,0))
		
			msgim_center_x, msgim_center_y = msg_image.get_size()
			msgim_center_x //= 2
			msgim_center_y //= 2
		
			self.screen.blit(msg_image, (
			  self.width // 2-msgim_center_x,
			  self.height // 2-msgim_center_y+i*22))
	
	def draw_matrix(self, matrix, offset):
		off_x, off_y  = offset
		for y, row in enumerate(matrix):
			for x, val in enumerate(row):
				if val:
					pygame.draw.rect(
						self.screen,
						colors[val],
						pygame.Rect(
							(off_x+x) *
							  cell_size,
							(off_y+y) *
							  cell_size, 
							cell_size,
							cell_size),0)
	
	def add_cl_lines(self, n):
		linescores = [0, 40, 100, 300, 1200]
		self.lines += n
		self.score += linescores[n] * self.level
		if self.lines >= self.level*6:
			self.level += 1
			newdelay = 1000-50*(self.level-1)
			newdelay = 100 if newdelay < 100 else newdelay
			pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
	
	def move(self, delta_x):
		if not self.gameover and not self.paused:
			new_x = self.stone_x + delta_x
			if new_x < 0:
				new_x = 0
			if new_x > cols - len(self.stone[0]):
				new_x = cols - len(self.stone[0])
			if not check_collision(self.board,
					       self.stone,
					       (new_x, self.stone_y)):
				self.stone_x = new_x
	def quit(self):
		self.center_msg("Exiting...")
		pygame.display.update()
		sys.exit()
	
	def drop(self, manual):
		if not self.gameover and not self.paused:
			self.score += 1 if manual else 0
			self.stone_y += 1
			if check_collision(self.board,
					   self.stone,
					   (self.stone_x, self.stone_y)):
				self.board = join_matrixes(
				  self.board,
				  self.stone,
				  (self.stone_x, self.stone_y))
				self.new_stone()
				cleared_rows = 0
				while True:
					for i, row in enumerate(self.board[:-1]):
						if 0 not in row:
							self.board = remove_row(
							  self.board, i)
							cleared_rows += 1
							break
					else:
						break
				self.add_cl_lines(cleared_rows)
				return True
		return False
	
	def insta_drop(self):
		if not self.gameover and not self.paused:
			while(not self.drop(True)):
				pass
	
	def rotate_stone(self):
		if not self.gameover and not self.paused:
			new_stone = rotate_clockwise(self.stone)
			if not check_collision(self.board,
					       new_stone,
					       (self.stone_x, self.stone_y)):
				self.stone = new_stone
	
	def toggle_pause(self):
		self.paused = not self.paused
	
	def start_game(self):
		if self.gameover:
			self.init_game()
			self.gameover = False	
	
	def run(self):
		key_actions = {
			'ESCAPE':	self.quit,
			'LEFT':		lambda:self.move(-1),
			'RIGHT':	lambda:self.move(+1),
			'DOWN':		lambda:self.drop(True),
			'UP':		self.rotate_stone,
			'p':		self.toggle_pause,
			'SPACE':	self.start_game,
			'RETURN':	self.insta_drop
		}
		
		self.gameover = False
		self.paused = False
		haveMoved = False
		highScore = 0
		movesExecuted = 0
		totalScore = 0
		averageScore = 0
		gamesPlayed = 0
		madeDecision = False
		
		dont_burn_my_cpu = pygame.time.Clock()
		while 1:
			self.screen.fill((0,0,0))
			if self.gameover:
				self.center_msg("""Game Over!\nYour score: %d
Press space to continue""" % self.score)
				gamesPlayed += 1
				totalScore += self.score
				averageScore = totalScore/gamesPlayed
				if self.score > highScore:
					highScore = self.score
					print('High Score: ',self.score)
					print('Lines: ',self.lines)
				if gamesPlayed % 10 == 0:
					print('Average Score: ', averageScore)
					print('Games played: ', gamesPlayed)
				key_actions['SPACE']()
			else:
				if self.paused:
					self.center_msg("Paused")
				else:
					pygame.draw.line(self.screen,
						(255,255,255),
						(self.rlim+1, 0),
						(self.rlim+1, self.height-1))
					self.disp_msg("Next:", (
						self.rlim+cell_size,
						2))
					self.disp_msg("Score: %d\n\nLevel: %d\
\nLines: %d" % (self.score, self.level, self.lines),
						(self.rlim+cell_size, cell_size*5))
					self.draw_matrix(self.bground_grid, (0,0))
					self.draw_matrix(self.board, (0,0))
					self.draw_matrix(self.stone,
						(self.stone_x, self.stone_y))
					self.draw_matrix(self.next_stone,
						(cols+1,2))
			pygame.display.update()
			
			for event in pygame.event.get():
				if event.type == pygame.USEREVENT+1:
					self.drop(False)
				elif event.type == pygame.QUIT:
					self.quit()
			#print('start the move')

			if madeDecision == False:
				theMove = check_move(self.board, self.stone, self.next_stone)
				#print('theMove',theMove)
				#print('stoneX',self.stone_x)
				madeDecision = True
			else:
				if theMove[0] > 0:
					key_actions['UP']()
					theMove[0] += -1
				elif theMove[1] > self.stone_x:
					key_actions['RIGHT']()
				elif theMove[1] < self.stone_x:
					key_actions['LEFT']()

				else:
					madeDecision = False
					#print('made the Move',theMove)
					key_actions['RETURN']()


					
			dont_burn_my_cpu.tick(maxfps)

if __name__ == '__main__':
	random.seed(42)
	App = TetrisApp()
	App.run()





	

#
# SimonSays.py
# Inspired by Etho
#
# Jonatan H Sundqvist
# February 11 2015
#

# TODO | - Better name (?)
#        -
#
# SPEC | - https://www.youtube.com/watch?v=lMlgFLK0mcY
#        -



from random import shuffle, choice
from enum import Enum
from collections import namedtuple

import tkinter as tk



def play(initial=4, cap=20):

	'''
	Play a game of Simon Says

	'''

	# TODO: Configurable 'problem' space
	# TODO: Other signals (eg. are there any more rounds)
	# TODO: Infinite feed (?)

	Colours = Enum('Colours', 'Red Green Yellow Blue')
	options = [c for c in Colours]

	yield options #

	for chain in range(initial, cap+1):
		sequence = [choice(options) for n in range(chain)] # Random sequence of colours
		remembered = yield sequence
		print('Yielded sequence and accepted guess: ', remembered)
		yield sequence == remembered #all((guess == right) for guess, right in zip(sequence, remembered)) # TODO: Compare with == (?)
		print('Yielded result')



class Simon(object):

	'''
	Docstring goes here

	'''

	Square = namedtuple('Option', 'tag fill pos highlighted') # Encapsulates data for each option (ties it to the UI)

	def __init__(self):

		'''
		Docstring goes here

		'''
		
		# TODO: Use pygame (?)
		# TODO: Animations, sound
		# TODO: Fancy interface
		# TODO: Configuration (cf. play)

		print('Simon Says do as I do and all will be well')

		# Game logic
		self.game = play()
		self.options  = next(self.game) # Retrieve all possible options
		self.sequence = None
		
		self.remembered = []

		# Gameplay configurations
		# TODO: Various delays
		self.delay = None

		# Gameplay flag
		# TODO: Use enum (?)
		self.responsive = False # Are we currently accepting input? TODO: Rename (?)
		self.ongoing    = False

		# Interface configurations

		# Interface configurations
		self.size   = namedtuple('Size', 'width height')(400, 400) # TODO: Magic attribute (?)
		self.centre = self.size.width//2, self.size.height//2      # TODO: Magic attribute (?)

		# Create and customise window
		self.frame = tk.Tk()
		self.frame.title('Simon Says')
		self.frame.geometry('{0}x{1}'.format(*self.size))
		self.frame.resizable(width=False, height=False)

		#
		self.canvas = tk.Canvas(width=self.size.width, height=self.size.height)
		self.canvas.pack()

		#
		# TODO: Font options
		# TODO: More versatile feedback (performance dependent)
		# TODO: Customisable font
		# TODO: Store messages (?)
		self.feedback = self.canvas.create_text(self.centre, text='Space to start', anchor=tk.CENTER, fill='black', font=('Tahoma', 32))

		#
		# TODO: Add configuration (don't hardcode options)
		width = self.centre[0] # Width of each square

		# TODO: Use self.squares to refactor this mess
		corners = ((0,0), (width,0), (0,width), (width,width))
		colours = ((0xFF, 0x0, 0x0), (0x0, 0xFF, 0x0), (0xEE, 0xFF, 0x12), (0x0, 0x0, 0xFF)) #('red', 'green', 'yellow', 'blue')

		# Mapping between options and associated data
		# TODO: Don't hardcode
		self.squares = {
			self.options[0] : self.createTile(corners[0], width, colours[0], (0xFF, 0x20, 0x20)),
			self.options[1] : self.createTile(corners[1], width, colours[1], (0x20, 0xFF, 0x20)),
			self.options[2] : self.createTile(corners[2], width, colours[2], (0xFF, 0xFF, 0x32)),
			self.options[3] : self.createTile(corners[3], width, colours[3], (0x20, 0x20, 0xFF))
		}


	def say(self):

		'''
		Docstring goes here

		'''
		
		pass


	def onLeftDown(self):

		'''
		Docstring goes here

		'''
		
		pass


	def onLeftUp(self):

		'''
		Docstring goes here

		'''
		
		pass


	def onSpace(self, event):

		'''
		Docstring goes here

		'''

		pass


	def createTile(self, pos, width, fill, highlight):

		'''
		Docstring goes here

		'''
		
		tag = self.canvas.create_rectangle(pos, (pos[0]+width, pos[1]+width), fill='#%02x%02x%02x' % fill) # Canvas ID
		return Simon.Square(tag, fill, pos, highlight)


	def highlight(self, square, reset=True):
		
		'''
		Docstring goes here

		'''

		# TODO: Additonal configuration (?)
		clamp = lambda val, mn=0, mx=255: sorted((mn, mx, val))[1]
		RGB = lambda r,g,b: '#%02X%02X%02X' % (clamp(int(r)), clamp(int(g)), clamp(int(b))) #



	def reset(self, square):
		# TODO: Better name (?)
		self.highlight(square, reset=True)



def main():
	
	'''
	Docstring goes here

	'''

	simon = Simon()
	simon.play()



if __name__ == '__main__':
	main()
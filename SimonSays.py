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
		self.frame.geometry('{0}x{1}'.format(*size))
		self.frame.resizable(width=False, height=False)

		#
		self.canvas = tk.Canvas(width=self.size.width, height=self.size.height)
		self.canvas.pack()

		#
		# TODO: Font options
		# TODO: More versatile feedback (performance dependent)
		# TODO: Customisable font
		# TODO: Store messages (?)
		self.feedback = self.canvas.create_text(centre, text='Space to start', anchor=tk.CENTER, fill='black', font=('Tahoma', 32))

		#
		# TODO: Add configuration (don't hardcode options)
		width = size.centre[0] # Width of each square

		# TODO: Use self.squares to refactor this mess
		corners = ((0,0), (width,0), (0,width), (width,width))
		colours = ((0xFF, 0x0, 0x0), (0x0, 0xFF, 0x0), (0xEE, 0xFF, 0x12), (0x0, 0x0, 0xFF)) #('red', 'green', 'yellow', 'blue')

		# Mapping between options and associated data
		# TODO: Don't hardcode
		self.squares = {
			self.options.Red    : self.createTile(corners[0], width, colours[0], (0xFF, 0x20, 0x20)),
			self.options.Green  : self.createTile(corners[1], width, colours[1], (0x20, 0xFF, 0x20)),
			self.options.Yellow : self.createTile(corners[2], width, colours[2], (0xFF, 0xFF, 0x32)),
			self.options.Blue   : self.createTile(corners[3], width, colours[3], (0x20, 0x20, 0xFF))
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
		
		tag = canvas.create_rectangle(pos, (pos[0]+width, pos[1]+width), fill='#%02x%02x%02x' % fill) # Canvas ID
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



def interact():

	'''
	User interaction for the Simon Says game

	'''

	# TODO: Use pygame (?)
	# TODO: Animations, sound
	# TODO: Fancy interface
	# TODO: Configuration (cf. play)

	print('Simon Says do as I do and all will be well')

	# Game logic
	game = play()

	# Configurations
	size = namedtuple('Size', 'width height')(400, 400)

	# Create and customise window
	frame = tk.Tk()
	frame.title('Simon Says')
	frame.geometry('{0}x{1}'.format(*size))
	frame.resizable(width=False, height=False)

	#
	canvas = tk.Canvas(width=size.width, height=size.height)
	canvas.pack()

	#
	width = size.width//2 # Width of each square

	corners = ((0,0), (width,0), (0,width), (width,width))
	colours = ((0xFF, 0x0, 0x0), (0x0, 0xFF, 0x0), (0xEE, 0xFF, 0x12), (0x0, 0x0, 0xFF)) #('red', 'green', 'yellow', 'blue')
	red, green, yellow, blue = (canvas.create_rectangle(pos, (pos[0]+width, pos[1]+width), fill='#%02x%02x%02x'%col) for pos, col in zip(corners, colours))
	squares = red, green, yellow, blue

	# red.value, green.value, yellow.value, blue.value = next(game) # TODO: Save options somewhere else (?)

	#
	options = next(game) #

	fromID = dict(zip(squares, options)) # TODO: Rename (?)
	fromOp = dict(zip(options, squares)) # TODO: Rename (from option) (?)

	clamp = lambda val, mn=0, mx=255: sorted((mn, mx, val))[1]
	RGB = lambda r,g,b: '#%02X%02X%02X' % (clamp(int(r)), clamp(int(g)), clamp(int(b))) #

	class State:
		# TODO: Rename (?)
		remembered = []
		sequence = next(game) #
		ongoing = False
		message = canvas.create_text((size.width//2, size.height//2), text='Space to start', anchor=tk.CENTER, fill='black', font=('Tahoma', 35))

	print('First sequence: ', State.sequence)

	# TODO: Suspend guessing meanwhile
	def show(items):
		# TODO: Deal with async issues (crops up all the time...)
		# TODO: whenDone callback (?)
		# TODO: Rename arguments (?)
		item, rest = items[0], items[1:]
		highlight(item, fromOp[item], delta=40)

		def shownext():
			# TODO: Un-nest (?)
			reset(item, fromOp[item], delta=40)
			if len(rest) > 0:
				frame.after(150, lambda: show(rest)) # Wait before showing the next

		frame.after(400, shownext)

	def highlight(option, ID, delta=40):
		# TODO: Utility for manipulating colours
		# TODO: Don't hardcode values
		fill = canvas.itemcget(ID, 'fill') # TODO: Don't hardcode deltas
		r, g, b = int(fill[1:3], 16), int(fill[3:5], 16), int(fill[5:7], 16)
		canvas.itemconfig(ID, fill=RGB(r+delta,g+delta,b+delta)) # TODO: Handle invalid

	def reset(option, ID, delta=40):
		# Opposite of highlight
		highlight(option, ID, delta=-delta)

	def space(event):
		if not State.ongoing:
			# TODO: Countdown
			print('New round...')
			canvas.itemconfig(State.message, state=tk.HIDDEN)
			State.ongoing = True
			frame.after(200, lambda: show(State.sequence)) # Another round

	def click(option, ID, down=True):
		def onclick(ev):
			# TODO: Check if we're ready to accept input
			if not down:
				reset(option, ID)
				return

			if not State.ongoing:
				return

			highlight(option, ID)
			State.remembered.append(option)
			if len(State.remembered) == len(State.sequence):
				correct = game.send(State.remembered)
				# TODO: Graphical feedback
				# TODO: Performance-dependent feedback (eg. length of chain, delay)
				# TODO: Feedback code when you release (?)
				if correct:
					print('Hurray! You remembered correctly')
					canvas.itemconfig(State.message, text='Hurray!')
				else:
					print('You\'re supposed to do as I do!')
					canvas.itemconfig(State.message, text='Embarrassing...')
				State.sequence = next(game) # TODO: Check if it has next
				State.remembered = []
				print('Press space to continue')
				State.ongoing = False
				canvas.itemconfig(State.message, state=tk.NORMAL)
				frame.after(1500, lambda: canvas.itemconfig(State.message, text='Space to start'))
				# frame.after(1500, lambda: show(State.sequence)) # Another round
		return onclick

	for option, ID in zip(options, (red, green, yellow, blue)):
		canvas.tag_bind(ID, '<1>', func=click(option, ID, down=True))
		canvas.tag_bind(ID, '<ButtonRelease-1>', func=click(option, ID, down=False)) # Reset colour

	frame.bind('<space>', space)
	frame.mainloop()

	# for attempt in game:
		# game.send("hello")



def main():
	
	'''
	Docstring goes here

	'''

	interact()



if __name__ == '__main__':
	main()
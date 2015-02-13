#
# SimonSays.py
# Inspired by Etho
#
# Jonatan H Sundqvist
# February 11 2015
#

# TODO | - Better name (?)
#        - Stats
#        - Load settings, change during runtime (?1)
#        - Transitions when layout changes (eg. (x,y) -> (x', y'), )
#        - Hotkeys (1-9) (?)

# SPEC | - https://www.youtube.com/watch?v=lMlgFLK0mcY
#        -


import tkinter as tk
import colorsys

from random import shuffle
from enum import Enum
from collections import namedtuple

from math import ceil

from logic import play



class Simon(object):

	'''
	Docstring goes here

	'''

	Square = namedtuple('Option', 'option tag fill pos highlighted') # Encapsulates data for each option (ties it to the UI)

	def __init__(self):

		'''
		Docstring goes here

		'''
		
		# TODO: Use pygame (?)
		# TODO: Animations, sound
		# TODO: Fancy interface
		# TODO: Configuration (cf. play)
		# TODO: Colour settings (contrast, theme, temperature, etc.)

		print('Simon Says do as I do and all will be good.')

		# Game logic
		self.initial = 4 #
		self.cap  = 20 #
		self.step = 1  #
		self.noptions = 4 # TODO: Rename (?)
		
		self.game = play(initial=self.initial, cap=self.cap, step=self.step, size=self.noptions)
		self.options  = next(self.game) # Retrieve all possible options
		self.sequence = next(self.game) #
		
		self.remembered = []

		# Gameplay configurations
		# TODO: Various delays
		self.resetDelay = 800 # (ms)
		self.nextDelay  = 350 # (ms)
		self.restartDelay = 1500 # (ms)
		self.startDelay   = 200

		# Gameplay flag
		# TODO: Use enum (?)
		self.responsive = False # Are we currently accepting input? TODO: Rename (?)
		self.ongoing    = False

		# Interface configurations

		# Interface configurations
		# TODO: Adapt size and aspect ratio
		self.size   = namedtuple('Size', 'width height')(400, 400) # TODO: Magic attribute (?)
		self.centre = self.size.width//2, self.size.height//2      # TODO: Magic attribute (?)
		
		self.rowsize = ceil(self.noptions**0.5)
		
		# Create and customise window
		self.frame = tk.Tk()
		self.frame.title('Simon Says')
		self.frame.geometry('{0}x{1}'.format(*self.size))
		self.frame.resizable(width=False, height=False)

		#
		self.canvas = tk.Canvas(width=self.size.width, height=self.size.height)
		self.canvas.pack()

		#
		# TODO: Add configuration (don't hardcode options)
		width = self.size.width//self.rowsize # Width of each square

		# TODO: Use self.squares to refactor this mess
		colours = (0xBB, 0x0, 0x0), (0x0, 0xBB, 0x0), (0xBB, 0xBB, 0x12), (0x0, 0x0, 0xBB) #('red', 'green', 'yellow', 'blue')
		colours = [tuple(ch*255 for ch in colorsys.hsv_to_rgb(h/255, 0.8, 0.8)) for h in range(0, 255)]
		shuffle(colours)
		# Mapping between options and associated data
		# TODO: Don't hardcode
		pos = lambda index: (index%self.rowsize*width, index//self.rowsize*width)
		self.squares = { option : self.createTile(option, pos(i), width, colours[i], dimmer(colours[i], 1.4)) for i, option in enumerate(self.options) }

		#
		# We need to create the text after the squares, due to stacking (or move it up manually)
		# TODO: Font options
		# TODO: More versatile feedback (performance dependent)
		# TODO: Customisable font
		# TODO: Store messages (?)
		self.feedback = self.canvas.create_text((self.centre[0], self.centre[1]), text='Space to start', anchor=tk.CENTER, fill='black', font=('Tahoma', 32))


		# And lastly, bind events
		for n, (option, square) in enumerate(self.squares.items(), 1):
			self.canvas.tag_bind(square.tag, '<1>',               func=lambda e, square=square: self.onLeftDown(e, square))  #
			self.canvas.tag_bind(square.tag, '<ButtonRelease-1>', func=lambda e, square=square: self.onLeftUp(e, square))    # Reset colour

			self.frame.bind('%d' % n,              func=lambda e, square=square: self.onLeftDown(e, square))  #
			self.frame.bind('<KeyRelease-%d>' % n, func=lambda e, square=square: self.onLeftUp(e, square))    # Reset colour

		self.frame.bind('<space>', lambda e: self.onSpace(e))



	def say(self, sequence, done=None):

		'''
		Instructs Simon to 'say' something

		'''

		# TODO: Suspend guessing meanwhile (✓)
		# TODO: Deal with async issues (crops up all the time...) (✓)
		# TODO: whenDone callback (✗)
		# TODO: Rename arguments (✗)
		self.responsive = False # Suspend input
		self.highlight(self.squares[sequence[0]])

		def shownext():
			# TODO: Un-nest (?)
			self.unhighlight(self.squares[sequence[0]])
			if len(sequence) > 1:
				self.frame.after(self.nextDelay, lambda: self.say(sequence[1:])) # Wait before showing the next
			else:
				self.responsive = True # Re-enable input

		self.frame.after(self.resetDelay, shownext)


	def onLeftDown(self, event, square):

		'''
		Docstring goes here

		'''
		
		# Check if we're ready to accept input
		if not (self.responsive and self.ongoing):
			return

		self.highlight(square) #


	def onLeftUp(self, event, square):

		'''
		Docstring goes here

		'''

		# TODO: Check if we're ready to accept input
		if not (self.responsive and self.ongoing):
			return

		self.unhighlight(square)
		self.remembered.append(square.option)

		if len(self.remembered) == len(self.sequence):
			
			# TODO: Graphical feedback
			# TODO: Performance-dependent feedback (eg. length of chain, delay)
			# TODO: Feedback code when you release (?)
			correct = self.game.send(self.remembered)

			if correct:
				print('Hurray! You remembered correctly')
				self.canvas.itemconfig(self.feedback, text='Hurray!')
			else:
				print('You\'re supposed to do as I do!')
				self.canvas.itemconfig(self.feedback, text='Embarrassing...')
			
			# Update game state (new round)
			self.reset()


	def reset(self):
		
		'''
		Resets the game and prepares for a new round

		'''

		# TODO: Move to method (✓)
		self.sequence = next(self.game) # TODO: Check if it has next
		self.remembered = []
		print('Press space to continue')
		self.ongoing    = False #
		self.responsive = False # No longer accepting 'guesses'
		self.canvas.itemconfig(self.feedback, state=tk.NORMAL)
		self.frame.after(self.restartDelay, lambda: self.canvas.itemconfig(self.feedback, text='Space to start'))
		# TODO: Add delay setting (✓)


	def onSpace(self, event):

		'''
		Docstring goes here

		'''

		# TODO: Check other flags (?)
		# TODO: Do we need both flags (ongoing, responsive)
		if not self.ongoing:
			# TODO: Countdown
			print('New round...')
			self.canvas.itemconfig(self.feedback, state=tk.HIDDEN)
			self.ongoing = True
			# TODO: Add delay setting
			self.frame.after(self.startDelay, lambda: self.say(self.sequence)) # Another round


	def createTile(self, option, pos, width, fill, highlight):

		'''
		Docstring goes here

		'''
		
		tag = self.canvas.create_rectangle(pos, (pos[0]+width, pos[1]+width), fill='#%02x%02x%02x' % fill, width=0) # Canvas ID
		return Simon.Square(option, tag, fill, pos, highlight)


	def highlight(self, square, reset=False):
		
		'''
		Docstring goes here

		'''

		# TODO: Additonal configuration (?)
		fill = '#%02x%02x%02x' % (square.fill if reset else square.highlighted)
		self.canvas.itemconfig(square.tag, fill=fill)


	def unhighlight(self, square):
		# TODO: Better name (?)
		self.highlight(square, reset=True)


	def play(self):

		'''
		Docstring goes here

		'''

		self.frame.mainloop()



def dimmer(rgb, coefficient):
	clamp = lambda val, mn=0, mx=255: sorted((mn, mx, val))[1]
	r, g, b = rgb
	h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
	r, g, b = colorsys.hsv_to_rgb(h, s, v*coefficient)
	return clamp(r*255), clamp(g*255), clamp(b*255)


def main():
	
	'''
	Docstring goes here

	'''

	simon = Simon()
	simon.play()



if __name__ == '__main__':
	main()
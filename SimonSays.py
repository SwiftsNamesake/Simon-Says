#
# SimonSays.py
# Inspired by Etho
#
# Jonatan H Sundqvist
# February 11 2015
#

# TODO | - Better name (?)
#        - Stats
#        - Load settings, change during runtime (?)

# SPEC | - https://www.youtube.com/watch?v=lMlgFLK0mcY
#        -


import tkinter as tk

from enum import Enum
from collections import namedtuple

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

		print('Simon Says do as I do and all will be well')

		# Game logic
		self.game = play()
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
		# TODO: Add configuration (don't hardcode options)
		width = self.centre[0] # Width of each square

		# TODO: Use self.squares to refactor this mess
		corners = ((0,0), (width,0), (0,width), (width,width))
		colours = ((0xCC, 0x0, 0x0), (0x0, 0xCC, 0x0), (0xEE, 0xCC, 0x12), (0x0, 0x0, 0xCC)) #('red', 'green', 'yellow', 'blue')

		# Mapping between options and associated data
		# TODO: Don't hardcode
		self.squares = {
			self.options[0] : self.createTile(self.options[0], corners[0], width, colours[0], (0xFF, 0x20, 0x20)),
			self.options[1] : self.createTile(self.options[1], corners[1], width, colours[1], (0x20, 0xFF, 0x20)),
			self.options[2] : self.createTile(self.options[2], corners[2], width, colours[2], (0xFF, 0xFF, 0x32)),
			self.options[3] : self.createTile(self.options[3], corners[3], width, colours[3], (0x20, 0x20, 0xFF))
		}

		#
		# We need to create the text after the squares, due to stacking (or move it up manually)
		# TODO: Font options
		# TODO: More versatile feedback (performance dependent)
		# TODO: Customisable font
		# TODO: Store messages (?)
		self.feedback = self.canvas.create_text(self.centre, text='Space to start', anchor=tk.CENTER, fill='black', font=('Tahoma', 32))


		# And lastly, bind events
		for option, square in self.squares.items():
			self.canvas.tag_bind(square.tag, '<1>',               func=lambda e, square=square: self.onLeftDown(e, square))  #
			self.canvas.tag_bind(square.tag, '<ButtonRelease-1>', func=lambda e, square=square: self.onLeftUp(e, square))    # Reset colour

		self.frame.bind('<space>', lambda e: self.onSpace(e))



	def say(self, sequence, done=None):

		'''
		Instructs Simon to 'say' something

		'''

		# TODO: Suspend guessing meanwhile
		# TODO: Deal with async issues (crops up all the time...)
		# TODO: whenDone callback (?)
		# TODO: Rename arguments (?)
		self.responsive = False # Suspend input
		self.highlight(self.squares[sequence[0]])

		def shownext():
			# TODO: Un-nest (?)
			self.reset(self.squares[sequence[0]])
			if len(sequence) > 1:
				self.frame.after(self.nextDelay, lambda: self.say(sequence[1:])) # Wait before showing the next
			else:
				self.responsive = True # Re-enable input
				# done()

		self.frame.after(self.resetDelay, shownext)


	def onLeftDown(self, event, square):

		'''
		Docstring goes here

		'''
		
		# TODO: Check if we're ready to accept input
		if not self.responsive:
			return
		elif not self.ongoing:
			return

		self.highlight(square) #

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
			# TODO: Move to method (?)
			self.sequence = next(self.game) # TODO: Check if it has next
			self.remembered = []
			print('Press space to continue')
			self.ongoing    = False #
			self.responsive = False # No longer accepting 'guesses'
			self.canvas.itemconfig(self.feedback, state=tk.NORMAL)
			self.frame.after(self.restartDelay, lambda: self.canvas.itemconfig(self.feedback, text='Space to start'))
			# TODO: Add delay setting
			# frame.after(1500, lambda: show(self.sequence)) # Another round


	def onLeftUp(self, event, square):

		'''
		Docstring goes here

		'''
		
		self.reset(square)


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
		
		tag = self.canvas.create_rectangle(pos, (pos[0]+width, pos[1]+width), fill='#%02x%02x%02x' % fill) # Canvas ID
		return Simon.Square(option, tag, fill, pos, highlight)


	def highlight(self, square, reset=False):
		
		'''
		Docstring goes here

		'''

		# TODO: Additonal configuration (?)
		# clamp = lambda val, mn=0, mx=255: sorted((mn, mx, val))[1]
		# RGB = lambda r,g,b: '#%02X%02X%02X' % (clamp(int(r)), clamp(int(g)), clamp(int(b))) #
		fill = '#%02x%02x%02x' % (square.fill if reset else square.highlighted)
		self.canvas.itemconfig(square.tag, fill=fill)


	def reset(self, square):
		# TODO: Better name (?)
		self.highlight(square, reset=True)


	def play(self):

		'''
		Docstring goes here

		'''

		self.frame.mainloop()



def main():
	
	'''
	Docstring goes here

	'''

	simon = Simon()
	simon.play()



if __name__ == '__main__':
	main()
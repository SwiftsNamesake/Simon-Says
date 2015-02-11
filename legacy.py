#
# Legacy.py
# Original (one-hour) implementation of Simon Says
#
# Jonatan H Sundqvist
# February 12 2015
#

# TODO | -
#        -
#
# SPEC | -
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
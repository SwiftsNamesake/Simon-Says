#
# Simon Says - Logic-py
# Implements the gameplay for Simon Says
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
		yield sequence == remembered #all((guess == right) for guess, right in zip(sequence, remembered)) # TODO: Compare with == (?)



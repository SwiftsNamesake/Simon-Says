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


from enum import Enum
from random import randint



def play(initial=4, cap=20, step=1, size=4):

	'''
	Play a game of Simon Says

	'''

	# TODO: Configurable 'problem' space
	# TODO: Other signals (eg. are there any more rounds)
	# TODO: Infinite feed (?)
	# TODO: Retry when failing (?)

	options = [c for c in range(size)]

	yield options #

	for chain in range(initial, cap+1, step):
		sequence = [randint(0, size-1) for n in range(chain)] # Random sequence of colours
		remembered = yield sequence
		yield sequence == remembered #all((guess == right) for guess, right in zip(sequence, remembered)) # TODO: Compare with == (?)



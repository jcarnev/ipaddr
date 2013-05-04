#!/usr/bin/env python

''' 
binutils.py - Mixin class that provides basic utilities for the ipaddr library. 
Only utilities that are not specific to any addressing space should be added
to this class.
'''
import re, bitstring

class BinUtils(object):
	''' Mixin class containing basic conversion utilies that are not
	specific to any addressing scheme. '''
	
	@staticmethod
	def addressHex(address):
		''' Convert an address from bitstring to hexidecimal string 
		>>>> iputils.addressHex('0b11010011')
		'0xD3'
		'''
		try:
			return hex(int(address, 2))
		except ValueError as e:
			return e
		except TypeError as e:
			return e

	@staticmethod
	def addressBin(address):
		''' Convert an address from hexidecimal string or int to
		bitstring.

		>>>> iputils.addressBin('0xD3')
		'0b11010011'
		>>>> iputils.addressBin(6123)
		'0b00000000000000000001011111101011'
		'''

		try:
			if isinstance(address, int):
				return bin(int(address))
			else:
				if address[0:2] == '0b':
					return address
				elif address[0:2] == '0x':
					return bin(int(address, 16))
				else:
					raise ValueError
		except ValueError as e:
			return e





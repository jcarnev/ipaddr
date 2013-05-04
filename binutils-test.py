#!/usr/bin/env python

import unittest
import binutils

class TestConvertBinStingtoHex(unittest.TestCase):

	def setUp(self):
		self.seq = ['0b11010011', '0b000000001111111100001111', '0b11011111110000000000000100000001'] 

	def test_hex(self):
		for address in self.seq:
			hexvalue = binutils.BinUtils.addressHex(address)
			self.assertEqual(hexvalue, hex(int(address, 2)))
			print('%s => %s' % (hexvalue, hex(int(address, 2))))

				

if __name__ == '__main__':
	unittest.main()



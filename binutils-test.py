#!/usr/bin/env python

import unittest
import binutils

class TestConvertBinStingtoHex(unittest.TestCase):

	def setUp(self):
		self.seq = ['0b11010011', '0b000000001111111100001111', '0b11011111110000000000000100000001',
				'0b11111111111100001111111100000001'] 

	def test_hex(self):
		for address in self.seq:
			hexvalue = binutils.BinUtils.addressHex(address)
			self.assertEqual(hexvalue, hex(int(address, 2)))

				

class TestConverthextobinString(unittest.TestCase):

	def setUp(self):
		self.seq = ['0xd3d2', '0xff00', '0xabcd', '0xff2388220010']

	def test_hex_to_bin(self):
		for address in self.seq:
			binvalue = binutils.BinUtils.addressBin(address)
			self.assertEqual(binvalue, bin(int(address, 16)))

class TestConvertinttobin(unittest.TestCase):

	def setUp(self):
		self.seq = [123455667, 6123, 10001]

	def test_int_to_bin(self):
		for address in self.seq:
			binvalue = binutils.BinUtils.addressBin(address)
			self.assertEqual(binvalue,  bin(int(address)))


class TestConvertbintobin(unittest.TestCase):

	def setUp(self):
		self.seq =  ['0b11010000', '0b101001010']

	
	def test_bin_to_bin(self):
		for address in self.seq:
			binvalue = binutils.BinUtils.addressBin(address)
			self.assertEqual(binvalue, address)



if __name__ == '__main__':
	unittest.main()



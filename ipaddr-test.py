#!/usr/bin/env python

import unittest, random, ipaddr

class TestSequenceFunctions(unittest.TestCase):

	def setUp(self):
		self.network = ipaddr.ipv4Addr(addr='192.168.1.0', mask='255.255.255.0')
		self.hostRange = range(1, 255)

	def test_networkAddress(self):
		self.assertEqual('192.168.1.0', self.network.networkAddress)

	def test_networkMask(self):
		self.assertEqual('255.255.255.0', self.network.networkMask)

	def test_hostRange(self):
		self.netDataSet = []
		for address in self.network:
			self.netDataSet.append(address)
		self.testData = zip(self.netDataSet, self.hostRange)
		
		for host, testValue in self.testData:
			host = host.split('.')[3]
			self.assertEqual(host, str(testValue))

if __name__ == '__main__':
    unittest.main()
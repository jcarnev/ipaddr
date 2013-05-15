#!/usr/bin/env python

import ipv4utils

class AddressSpace(object):

    version = '0.1'
    
    minNetMaskLen = 1
    maxNetMaskLen = 32
    # create a dictionary of lists to track the subnet classes and subnet allocated
    # mark off any tht would also not be available so overlap doesn't happen
    #subnetsAllocated = {1: [], 2: []}
    

    __init__(self, AF_Family='IPv4', netAddr, netMask):
        self.AF_Family = AF_Family
        self.NetAddr = NetAddr
        self.NetMask = NetMask

    __str__(self):
        pass

    __repr__(self):
        pass

    __iter__(self):
        pass

    __len__(self):
        pass

    @property
    def broadcastAddr(self):
        pass

    @property
    def allSubnetsAddr(self):
        pass

    @property
    def NetworkClass(self):
        pass

    @property
    def NetworkInverseMask(self):
        pass

    def inNetwork(self):
        pass

    def maxPrefix(self):
        return maxNetMaskLen

    def minPrefix(self):
        return minNetMaskLen

    def addressFamily(self):
        return self.AF-Family

    def printNetDetails(self):
        pass

class subnets(object):

    version = '0.1'

    __init__(self, subnetAddr, subnetMask):
        self.subnetAddr = subnetAddr
        self.subnetMask = subnetMask

    __str__(self):
        pass

    __repr__(self):
        pass

    def inSubnet(self):
        pass
    
    
 

    

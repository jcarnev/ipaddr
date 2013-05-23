#!/usr/bin/env python

import ipv4utils, binutils 

class AddressSpace(binutils.BinUtils, object):

    version = '0.1'
    
    _minNetMaskLen = 1
    _maxNetMaskLen = 32
    # create a dictionary of lists to track the subnet classes and subnet allocated
    # mark off any tht would also not be available so overlap doesn't happen
    #subnetsAllocated = {1: [], 2: []}
    

    def __init__(self,  netAddr, netMask, AF_Family='IPv4'):
        self._AF_Family = AF_Family
        self._netAddr = ipv4utils.dotDecimalToBinStr(netAddr)
        self._netMask = ipv4utils.dotDecimalToBinStr(netMask)

    # __str__(self):
    #     pass

    # __repr__(self):
    #     pass

    @property 
    def networkAddress(self):
        '''Displays the network address in dotted decimal Format'''

        return ipv4utils.printDotDec(self._netAddr)

    @property 
    def networkMask(self):
        '''Displays the network mask in dotted decimal format'''

        return ipv4utils.printDotDec(self._netMask)

    @property 
    def inverseMask(self):
        '''Displays the inverse network mask in dotted decimal format'''

        return ipv4utils.printDotDec(self.networkInverseMask)

    @property 
    def addressFamily(self):
        ''' Displays the address family of the network address '''

        return self._AF_Family

    @property
    def broadcastAddr(self):
        '''Calculate the Broadcast address from network address'''
        network = self._netAddr
        # return ipv4utils.printDotDec(self.addressBin(int(self._netAddr, 2) | int(self.networkInverseMask, 2)))
        pass
        
    @property
    def allSubnetsAddr(self):
        '''Calulate the all subnets address using the network address
        and network mask '''
        pass

    @property
    def NetworkClass(self):
        '''Return the network class; Class A, Class B, Class C. Given a
        bitstring representation of a network address look at the first
        octet and determines the Class the address belongs to.'''

    @property
    def networkInverseMask(self):
        '''Given an IPv4 Network Mask as a bitstring, convert the
        mask to the inverse representation.
        1111111100000000 becomes 0000000011111111'''

        invMask = []
        if ipv4utils.isBinStr(self._netMask):
            for value in self._netMask:
                if value == '1':
                    invMask.append('0')
                else:
                    invMask.append('1')
            self._networkInverseMask = ''.join(invMask)
            return self._networkInverseMask
        else:
            return None


    def inNetwork(self):
        pass

    @property 
    def maxPrefixLen(self):
        return self._maxNetMaskLen

    @property 
    def minPrefixLen(self):
        '''Return the larger of minNetMaskLen or maskLen(self.NetMask)'''
        if (self.maskLen(self._netMask)) > self._minNetMaskLen:
            return self.maskLen(self._netMask)
        else:
            return self._minNetMaskLen

    def addressFamily(self):
        return self._AF_Family

    def printNetDetails(self):
        pass

class subnets(object):

    version = '0.1'

    def __init__(self, subnetAddr, subnetMask):
        self.subnetAddr = subnetAddr
        self.subnetMask = subnetMask

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        pass

    def inSubnet(self):
        pass
    
    
 

    

#!/usr/bin/env python

import ipv4utils, binutils 

class AddressSpace(object):

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
    def allSubnetsAddr(self):
        '''Calulate the all subnets address using the network address
        and network mask '''
        return self.networkAddress

    @property
    def networkClass(self):
        '''Return the network class; Class A, Class B, Class C. Given a
        bitstring representation of a network address look at the first
        octet and determines the Class the address belongs to.'''

        # Class A = First Byte 00000000 - 01111111
        # Class B = First Byte 10000000 - 10111111
        # class C = First Byte 11000000 - 11011111
        # class D = First Byte 11100000 - 11101111
        # class E = First Byte 11110000 - 11111111

        if self._netAddr[0] == '0':
            return 'Class A'
        elif self._netAddr[0:2] == '10':
            return 'Class B'
        elif self._netAddr[0:3] == '110':
            return 'Class C'
        elif self._netAddr[0:4] == '1110':
            return 'Class D'
        elif self._netAddr[0:4] == '1111':
            return 'Class E'
        else:
            raise ValueError

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

    @property 
    def maxPrefixLen(self):
        return self._maxNetMaskLen

    @property 
    def minPrefixLen(self):
        '''Return the larger of minNetMaskLen or maskLen(self.NetMask)'''
        if (self.maskLen) > self._minNetMaskLen:
            return self.maskLen
        else:
            return self._minNetMaskLen

    @property
    def broadcastAddr(self):
        '''Calculate the Broadcast address from network address'''
        
        baseMask = '1' * 32
        return ipv4utils.printDotDec(self._netAddr[0:self.maskLen] + baseMask[self.maskLen:])  
            
    @property
    def addressFamily(self):
        return self._AF_Family

    def _getNetData(self):
        ''' Retrieve properties of this address space and return the properties as a 
        dictionary for printing or data manipulation '''


        properties = ['Network Address', 'Network Mask', 'Network Mask Len', 'Broadcast Address',
        'All Subnets Address', 'From Network Class', 'Inverse Network Mask']

        data = [self.networkAddress, self.networkMask, str(self.maskLen), self.broadcastAddr, 
        self.allSubnetsAddr, self.networkClass, self.inverseMask]

        netData = dict(zip(properties, data))
        return netData


    def printNetDetails(self):
        ''' print network properties to stdout'''

        for (key, value) in self._getNetData().items():
            print('%s => %s' % (key, value))

    @property
    def maskLen(self):
        ''' Given a bitstring for a bitmask convert from bitstring to the 
        decimal number representing the number of 1's in the mask. 

        >>>>masklen('0b11110000', 8)
        4
        '''

        decimalMaskLen = 0
        assert len(self._netMask) <= self.maxPrefixLen
        tmpBitMask = int(self._netMask.rstrip('0'), 2)
        while tmpBitMask:
            tmpBitMask >>= 1
            decimalMaskLen += 1
        return decimalMaskLen

    def inNetwork(self):
        pass

    def __ge__:
        pass

    def __le__:
        pass

    def __eq__:
        pass

    def __ne__:
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
    
    
 

    

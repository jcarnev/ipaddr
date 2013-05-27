#!/usr/bin/env python

import re

# factory function to parse different IPv4 notations and return the appropriate class
# object

def __ge__(prefix1, prefix2):
        ''' Return True if prefix 1 is larger than prefix 2'''
        prefix1 = IPv4Utils.dotDec2Int(prefix1)
        prefix2 = IPv4Utils.dotDec2Int(prefix2)
        if prefix1 > prefix2:
            return True
        else:
            return False

def __le__(prefix1, prefix2):
    ''' Return Truen if prefix 1 is less than prefix 2'''
    prefix1 = IPv4Utils.dotDec2Int(prefix1)
    prefix2 = IPv4Utils.dotDec2Int(prefix2)
    if prefix1 < prefix2:
        return True
    else:
        return False

def __eq__(prefix1, prefix2):
    ''' Return True if prefix 1 and prefix 2 are equal'''
    prefix1 = IPv4Utils.dotDec2Int(prefix1)
    prefix2 = IPv4Utils.dotDec2Int(prefix2)
    if prefix1 == prefix2:
        return True
    else:
        return False

def __ne__(prefix1, prefix2):
    ''' Return True if prefix 1 and prefix 2 are not equal'''
    prefix1 = IPv4Utils.dotDec2Int(prefix1)
    prefix2 = IPv4Utils.dotDec2Int(prefix2)
    if prefix1 != prefix2:
        return True
    else:
        return False

def __add__(prefix1, value):
    ''' add value to the prefix to yield a new address '''
    prefix1 = IPv4Utils.dotDec2Int(prefix1)
    value = int(value)
    newValue = prefix1 + value
    addr = IPv4Utils.int2DotDec(newValue)
    return addr 

def __sub__(prefix1, value):
    ''' subtract value from prefix to yield a new address'''
    prefix1 = IPv4Utils.dotDec2Int(prefix1)
    value = int(value)
    newValue = prefix1 - value
    addr = IPv4Utils.int2DotDec(newValue)
    return addr 

def _parseNotation(*args):
    # match pattern for cidr notation, ex. 192.168.1.0/24
    cidr = re.compile(r'((([0-9]){1,3}(\.)*){4})/([0-9]{1,2})')
    # match pattern for address mask notation, ex. 192.168.1.0 255.255.255.0
    addrMask = re.compile(r'((([0-9]){1,3}(\.)*){4}) ((([0-9]){1,3}(\.)*){4})')
    # match pattern for hex network address and mask notation, ex. 0xC0A80100 0xFFFFFF00
    hexAddrMask = re.compile(r'(0x)(([0-9A-Fa-f]){8}) (0x)(([0-9A-Fa-f]){8})')
    
    # convert arg to single string object
    if len(args) == 2:
        args = args[0] + ' ' + args[1]
    else:
        args = args[0]
    # identify which notation was used 
    if cidr.match(args):
        result = cidr.match(args)
        return {'addr' : result.group(1), 'mask' : IPv4Utils._cidrMask2DotDec(result.group(5))}
    if addrMask.match(args):
        result = addrMask.match(args)
        return {'addr' : result.group(1), 'mask' : result.group(5)}
    if hexAddrMask.match(args):
        result = hexAddrMask.match(args)
        return {'addr' : IPv4Utils.hex2DotDec(result.group(2)), 'mask' : IPv4Utils.hex2DotDec(result.group(5))}



def validateArgs(kwargs):
    
    supportedAF = re.compile(r'ipv4')

    # validate that correct keywords have been used

    validArgs = ['addr', 'mask', 'af_family']

    # parse arguments
    if 1 <= len(kwargs) <= 3:
        for keyword in kwargs.keys():
            if keyword not in validArgs:
                raise ValueError, 'only keywords: addr, mask, af_family supported in ipvAddr()'

        if len(kwargs) == 3:
            # test to make sure address family is supported
            if not supportedAF.match(kwargs['af_family']):
                raise ValueError, '%s is not a supported address family' % af_family
            # Parse args and format to dotted decimal entry for both address and mask
            network = _parseNotation(kwargs['addr'].lower(), kwargs['mask'].lower())
            addr = network['addr']
            mask = network['mask']
            af_family = kwargs['af_family'].lower()
            
            # make sure that both address and mask are valid dotted decimal entries
            if not (IPv4Utils.isDotDec(addr) & (IPv4Utils.isDotDec(mask))):
                raise ValueError, 'Invalid IPv4 IP address and/or Mask'
            return (addr, mask, af_family)

        if len(kwargs) == 2:
            # set address family to IPv4 and assume that two arguments are address and mask
            af_family = 'ipv4'
            # parse args notation
            network = _parseNotation(kwargs['addr'].lower(), kwargs['mask'].lower())
            addr = network['addr']
            mask = network['mask']
            # make sure that both address and mask are valid dotted decimal entries
            if not (IPv4Utils.isDotDec(addr) & (IPv4Utils.isDotDec(mask))):
                raise ValueError, 'Invalid IPv4 IP address and/or Mask'
            return (addr, mask, af_family)

        if len(kwargs) == 1:
            # set address family to IPv4 and assume that cidr notation is being used
            af_family = 'ipv4'
            # parse args notation
            network = _parseNotation(kwargs['addr'].lower())
            addr = network['addr']
            mask = network['mask']
            if not (IPv4Utils.isDotDec(addr) & (IPv4Utils.isDotDec(mask))):
                raise ValueError, 'Invalid IPv4 IP address and/or Mask'
            return (addr, mask, af_family)
    else:
        raise ValueError, 'A valid IP network address and mask must be specified ex. ipaddr.ipv4Addr(addr="192.168.1.0", mask="255.255.255.0")'


def ipv4Addr(**kwargs):
    ''' This function accepts multiple input formats for IPv4 addressing and returns 
    a class object '''

    (addr, mask, af_family) = validateArgs(kwargs)
    return AddressSpace(addr, mask, af_family)
    
# Mixin class

class IPv4Utils():

    '''collection of utilities for managing IPv4 addresses'''

    @staticmethod
    def isHexStr(prefix):
        ''' Validate that an IPv4 prefix is in hexidecimal format; returns True/False '''
        prefix = prefix.lower()
        if prefix[0:2] == '0x':
                prefix = prefix[2:]
        hexset = {'a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        if (len(prefix)  == 8):
                for character in prefix[2:]:
                        if character not in hexset:
                                return False
                                break
                else:
                        return True
                
        else:
                return False

    @staticmethod
    def isBinStr(prefix):
            ''' Validate that a prefix is in binary string format. Returns True/False '''
            
            prefix = prefix.lower()
            binset = ['0', '1']
            if prefix[0:2] == '0b':
                    prefix = prefix[2:]
            if (type(prefix) == str) & (len(prefix) == 32):
                    
                    for character in prefix:
                            if character not in binset:
                                    return False
                                    break
                            else:
                                    return True
            else:
                    return False
                
        
    @staticmethod
    def isDotDec(prefix):
            ''' Validate that prefix is a valid IPv4 address and in dotted decimal format;
            return True/False
            '''
            maxOctets = 4
            octetsRead = 0

            for value in prefix.split('.'):
                    try:
                            value = int(value)
                    except ValueError:
                            return False

                    if octetsRead == 0:
                            try:
                                    assert 1 <= value <= 255, 'Prefix not a valid IPv4 dotted decimal address'
                            except:
                                    return False
                    else:
                            try:
                                    assert 0 <= value <= 255, 'Prefix not a valid IPv4 dotted decimal address'
                            except:
                                    return False
                    octetsRead += 1
            else:
                    if octetsRead > maxOctets:
                            return False
                    return True


    @staticmethod
    def _dec2Bin(octet):
            ''' Convert a decimal single octet value to its
            8 bit binary value.

            _dec2Bin(128)
            > '10000000'
            '''
            bits = []
            bitPositionValues = [128, 64, 32, 16, 8, 4, 2, 1]

            assert 0 <= octet <= 255

            if octet == 0:
                    return '00000000'
            else:
                    for value in bitPositionValues:
                            if octet / value:
                                    bits.append(str(1))
                                    octet -= value
                            else:
                                    bits.append(str(0))
                    return ''.join(bits)


    @staticmethod
    def _bin2Dec(bitstr):
            ''' Convert a binary string to decimal list that represents 4 octets '''

            if IPv4Utils.isBinStr(bitstr):
                    n = 8
                    return [str(int(bitstr[i:n+i], 2)) for i in range(0, len(bitstr), n)]
            else:
                    raise ValueError
            
                    
    @staticmethod
    def dotDecimalToBinStr(prefix):
            ''' Given an ipv4 address in dotted decimal
            format; 192.168.1.1, convert to a binary
            string.

            IdotDecimalToBinStr('192.168.1.1')
            > '11000000101010000000000100000001'
            '''

            binaddr = []
            if IPv4Utils.isDotDec(prefix):
                    octets = [int(octet) for octet in prefix.split('.')]
                    for octet in octets:
                            binaddr.append(IPv4Utils._dec2Bin(octet))
                    return ''.join(binaddr)
            else:
                    return None


    @staticmethod
    def hexToBinStr(prefix):
            ''' Given an ipv4 address in hexidecimal format; 0xc0a80101,
            convert it to a binary string.

            HexToBinStr('0xc0a80101')
            > '11000000101010000000000100000001'
            '''
            binaddr = []
            if prefix[0:2] == '0x':
                    prefix = prefix[2:]
            if IPv4Utils.isHexStr(prefix):
                    n = 2
                    octets = [int(prefix[i:n+i], 16) for i in range(0, len(prefix), n)]
                    for octet in octets:
                            binaddr.append(_dec2Bin(octet))
                    return ''.join(binaddr)
            else:
                    return None

    @staticmethod
    def hex2DotDec(prefix):
        ''' given an address or mask in hex format, convert to dotted decimal format'''
        
        if IPv4Utils.isHexStr(prefix):
            if prefix[0:2] == '0x':
                prefix = prefix[2:]
            a, b, c, d = prefix[0:2], prefix[2:4], prefix[4:6], prefix[6:8]
            # convert from hex to int and then into string
            a = str(int(a, 16))
            b = str(int(b, 16))
            c = str(int(c, 16))
            d = str(int(d, 16))
            addr = a, b, c, d
            addr = '.'.join(addr)
        return addr
        
    @staticmethod
    def int2DotDec(prefix):
        ''' Given an IPv4 address as an unsigned int representation, convert it to dotted 
        decimal format.'''

        assert type(prefix) == int
        binary = bin(prefix)
        # strip off the leading 0b 
        if binary[0:2] == '0b':
            binary = binary[2:]
        # binary conversion drops leading zeros, we need to add them back
        if len(binary) < 32:
            padding = 32 - len(binary)
            binary = ('0' * padding) + binary 
        # convert to decimal 
        addr = IPv4Utils._bin2Dec(binary)
        return '.'.join(addr)

    @staticmethod
    def _cidrMask2DotDec(mask):
        '''Given a mask length as an int, convert to the dotted decimal representation'''
        tmpMask = '1' * int(mask)
        padding = 32 - int(mask) 
        result = tmpMask + ('0' * padding)
        # convert to dotted decimal
        result = IPv4Utils._bin2Dec(result)
        result = '.'.join(result)
        return result

    @staticmethod
    def dotDec2Int(prefix):
        ''' Given an IPv4 inverse address mask, convert it to an unsigned int '''

        bitstring = ''
        for octet in prefix.split('.'):
            octet = int(octet)
            bits = IPv4Utils._dec2Bin(octet)
            bitstring += bits
        return int(bitstring, 2) 

    @staticmethod
    def convertAddr(prefix):
            ''' using functions above, parse to determine if address is hexidecimal, dotted decimal,
            or binary string; return binary format of address '''

            if IPv4Utils.isDotDec(prefix):
                    return IPv4Utils.dotDecimalToBinStr(prefix)
            if IPv4Utils.isHexStr(prefix):
                    return IPv4Utils.hexToBinStr(prefix)
            if IPv4Utils.isBinStr(prefix):
                    return prefix

    
    @staticmethod        
    def isLoopback(prefix):
            ''' Given an ipv4 address return True if the address is part of the
            reserved loopback address space 127.0.0.0/8, return False if the
            binary string is not part of the loopback address space. Supports
            Dotted Decimal, Hexidecimal or Binary String as input.

            011111110000000000000000000000000 -
            011111111111111111111111111111111

            isLoopback('0111111100000000
            0000000000000001')
            > True
            '''
            prefix = IPv4Utils.convertAddr(prefix)

            # Loopback space is any 127.0.0.0 address
            loopback = IPv4Utils._dec2Bin(127)

            if prefix[0:8] == loopback:
                    return True
            else:
                    return False
            

    @staticmethod
    def isMcast(prefix):
            ''' Given an ipv4 address in hexidecimal, dotted decimal or binary string format,
            test to see if the first octet falls in the multicast address range 224 - 239;
            return True/False.
            '''

            prefix = IPv4Utils.convertAddr(prefix)

            firstOctet = prefix[0:8]
            if int(firstOctet, 2) in range(224, 240):
                    return True
            else:
                    return False


    @staticmethod
    def isPrivateAddr(prefix):
            ''' Given an ipv4 address in hexidecimal, dotted decimal or binary string format,
            test to see if the first octet falls in any of the RFC1918 address space.
            192.168.0.0/16, 172.16.0.0 - 172.16.31.0/12 or 10.0.0.0/8.
            '''

            prefix = IPv4Utils.convertAddr(prefix)

            # test for 10.0.0.0/8
            if int(prefix[0:8], 2) == 10:
                    return True

            # test for 172.16.0.0 - 172.16.31.0/12
            if (int(prefix[0:8], 2) == 172) & (int(prefix[8:16], 2) == 16) & (int(prefix[16:24], 2) in range(0, 17)):
                    return True

            # test for 192.168.0.0/16
            if (int(prefix[0:8], 2) == 192) & (int(prefix[8:16], 2) == 168):
                    return True

            return False

    @staticmethod
    def isBogonAddr(prefix):
            ''' Given an ipv4 address in hexidecimal, dotted decimal, or binary string format,
            test to see if the address is one of the Bogon IP addresses:

            0.0.0.0/8
            10.0.0.0/8
            100.64.0.0/10
            127.0.0.0/8
            169.254.0.0/16
            172.16.0.0/12
            192.0.0.0/24
            192.0.2.0/24
            192.168.0.0/16
            198.18.0.0/15
            198.51.100.0/24
            203.0.113.0/24
            224.0.0.0/4
            240.0.0.0/4

            Retrun True/False
            '''
            pass

    @staticmethod
    def printDotDec(prefix):
            ''' Given an ipv4 address in hexidecimal, dotted decimal or binary string format,
            print the IPv4 address to stdout in dotted decimal format. '''

            if IPv4Utils.isDotDec(prefix):
                    return ('%s' % prefix)
            prefix = IPv4Utils.convertAddr(prefix)
            addr = IPv4Utils._bin2Dec(prefix)
            return '.'.join(addr)

class AddressSpace(IPv4Utils, object):

    version = '0.1'
    
    _minNetMaskLen = 1
    _maxNetMaskLen = 32
    # create a dictionary of lists to track the subnet classes and subnet allocated
    # mark off any tht would also not be available so overlap doesn't happen
    #subnetsAllocated = {1: [], 2: []}
    

    def __init__(self,  netAddr, netMask, AF_Family='IPv4'):
        self._AF_Family = AF_Family
        self._netAddr = IPv4Utils.dotDecimalToBinStr(netAddr)
        self._netMask = IPv4Utils.dotDecimalToBinStr(netMask)
        self._hosts = int(self._netAddr, 2) + 1

    # __str__(self):
    #     pass

    # __repr__(self):
    #     pass

    @property 
    def networkAddress(self):
        '''Displays the network address in dotted decimal Format'''

        return IPv4Utils.printDotDec(self._netAddr)

    @property 
    def networkMask(self):
        '''Displays the network mask in dotted decimal format'''

        return IPv4Utils.printDotDec(self._netMask)

    @property 
    def inverseMask(self):
        '''Displays the inverse network mask in dotted decimal format'''

        return IPv4Utils.printDotDec(self.networkInverseMask)

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
    def startHostAddr(self):
        '''Calculate and return the starting host IP address'''

        addr = IPv4Utils.dotDec2Int(self.networkAddress)
        addr += 1
        return IPv4Utils.int2DotDec(addr)

    @property
    def endHostAddr(self):
        ''' Calculate the last host address in the IP range '''

        baseAddr = IPv4Utils.dotDec2Int(self.networkAddress)
        inverse = IPv4Utils.dotDec2Int(self.inverseMask)
        endAddress = (baseAddr -1) + inverse
        return IPv4Utils.int2DotDec(endAddress) 

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
        if IPv4Utils.isBinStr(self._netMask):
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
        return IPv4Utils.printDotDec(self._netAddr[0:self.maskLen] + baseMask[self.maskLen:])  
            
    @property
    def addressFamily(self):
        return self._AF_Family

    @property 
    def hostRange(self):
        return '%s - %s' % (self.startHostAddr, self.endHostAddr)

    def _getNetData(self):
        ''' Retrieve properties of this address space and return the properties as a 
        dictionary for printing or data manipulation '''


        properties = ['Network Address', 'Network Mask', 'Network Mask Len', 'Broadcast Address',
        'All Subnets Address', 'Start Host Range', 'End Host Range', 'From Network Class', 'Inverse Network Mask']

        data = [self.networkAddress, self.networkMask, str(self.maskLen), self.broadcastAddr, 
        self.allSubnetsAddr, self.startHostAddr, self.endHostAddr, self.networkClass, self.inverseMask]

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

    def __iter__(self):
        return self

    def __getitem__(self):
        pass

    def next(self):
        value = self._hosts 
        if value > (int(self._netAddr, 2)) + (IPv4Utils.dotDec2Int(self.inverseMask) -1):
            raise StopIteration
        self._hosts += 1
        return IPv4Utils.int2DotDec(value) 

    def __len__(self):
        int(self.inverseMask.lstrip('0.')) - 1


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
    
    
 

    

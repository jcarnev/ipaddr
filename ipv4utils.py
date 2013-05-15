#!/usr/bin/env python

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

def isBinStr(prefix):
        ''' Validate that a prefix is in binary string format. Returns True/False '''
        
        prefix = prefix.lower()
        binset = ['0', '1']
        if prefix[0:2] == '0b':
                prefix = prefix[2:]
        if (type(test) == str) & (len(prefix) == 32):
                
                for character in prefix:
                        if character not in binset:
                                return False
                                break
                        else:
                                return True
        else:
                return False
                
        

def isDotDec(prefix):
        ''' Validate that prefix is a valid IPv4
        address and in dotted decimal format;
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


def dec2Bin(octet):
        ''' Convert a decimal single octet value to its
        8 bit binary value.

        dec2bin(128)
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


def bin2Dec(bitstr):
        ''' Convert a binary string to decimal list that represents 4 octets '''

        if isBinStr(bitstr):
                n = 8
                return [str(int(bitstr[i:n+i], 2)) for i in range(0, len(bitstr), n)]
        else:
                raise ValueError
        
                
def dotDecimalToBinStr(prefix):
        ''' Given an ipv4 address in dotted decimal
        format; 192.168.1.1, convert to a binary
        string.

        IdotDecimalToBinStr('192.168.1.1')
        > '11000000101010000000000100000001'
        '''

        binaddr = []
        if isDotDec(prefix):
                octets = [int(octet) for octet in prefix.split('.')]
                for octet in octets:
                        binaddr.append(dec2Bin(octet))
                return ''.join(binaddr)
        else:
                return None


def hexToBinStr(prefix):
        ''' Given an ipv4 address in hexidecimal format; 0xc0a80101,
        convert it to a binary string.

        HexToBinStr('0xc0a80101')
        > '11000000101010000000000100000001'
        '''
        binaddr = []
        if prefix[0:2] == '0x':
                prefix = prefix[2:]
        if isHexStr(prefix):
                n = 2
                octets = [int(prefix[i:n+i], 16) for i in range(0, len(prefix), n)]
                for octet in octets:
                        binaddr.append(dec2Bin(octet))
                return ''.join(binaddr)
        else:
                return None

def convertAddr(prefix):
        ''' using functions above, parse to determine if address is hexidecimal, dotted decimal,
        or binary string; return binary format of address '''

        if isDotDec(prefix):
                return dotDecimalToBinStr(prefix)
        if isHexStr(prefix):
                return hexToBinStr(prefix)
        if isBinStr(prefix):
                return prefix

        
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
        prefix = convertAddr(prefix)

        # Loopback space is any 127.0.0.0 address
        loopback = dec2Bin(127)

        if prefix[0:8] == loopback:
                return True
        else:
                return False
        

def isMcast(prefix):
        ''' Given an ipv4 address in hexidecimal, dotted decimal or binary string format,
        test to see if the first octet falls in the multicast address range 224 - 239;
        return True/False.
        '''

        prefix = convertAddr(prefix)

        firstOctet = prefix[0:8]
        if int(firstOctet, 2) in range(224, 240):
                return True
        else:
                return False


def isPrivateAddr(prefix):
        ''' Given an ipv4 address in hexidecimal, dotted decimal or binary string format,
        test to see if the first octet falls in any of the RFC1918 address space.
        192.168.0.0/16, 172.16.0.0 - 172.16.31.0/12 or 10.0.0.0/8.
        '''

        prefix = convertAddr(prefix)

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

def printDotDec(prefix):
        ''' Given an ipv4 address in hexidecimal, dotted decimal or binary string format,
        print the IPv4 address to stdout in dotted decimal format. '''

        if isDotDec(prefix):
                return ('%s' % prefix)
        prefix = convertAddr(prefix)
        addr = bin2Dec(prefix)
        return '.'.join(addr)




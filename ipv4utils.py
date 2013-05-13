#!/usr/bin/env python


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


def dotDecimalToBinStr(prefix):
        ''' Given an ipv4 address in dotted decimal
        format; 192.168.1.1, convert to a binary
        string.

        Ipv4Tools.dotDecimalToBinStr('192.168.1.1')
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



def isLoopback(prefix):
        ''' Given an ipv4 address as binary string
        return True if the address is part of the
        reserved loopback address space 127.0.0.0/8,
        return False if the binary string is not
        part of the loopback address space.

        011111110000000000000000000000000 -
        011111111111111111111111111111111

        Ipv4Tools.isLoopback('0111111100000000
        0000000000000001')
        > True
        '''

        # test that the variable is a 32 bit string
        assert (type(prefix) is str) & (len(prefix) == 32)

        # Loopback space is any 127.0.0.0 address
        loopback = dec2Bin(127)

        if prefix[0:8] == loopback:
                return True
        else:
                return False
        


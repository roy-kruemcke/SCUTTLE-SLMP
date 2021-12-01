# data.py
# Author: Roy Kruemcke (roanoake)
# 30 NOV 2021
# This class is for processing data, mainly used by L1_mpu to process data inputs.
# Honestly, there's probably libraries for this, but oh well.
# Lots of bit-banging and bitwise operations going on here.

def getSignedVal(num: int, bitSize: int):
    """
    Return the signed value of the number.
    :param num: unsigned integer value
    :param bitSize: length of the value in bits
    """
    mask = (2 ** bitSize) - 1
    if num & (1 << (bitSize - 1)):
        return num | ~mask
    else:
        return num & mask

# TODO:
# def countBits(num: int)
#   Returns the number of high bits in num
# def bytesToHexString(num: int, numBytes: int)
#   Returns a hexadecimal string of bytes

if __name__ == "__main__":
    n = 0x80
    print(n, '->', getSignedVal(n,8))

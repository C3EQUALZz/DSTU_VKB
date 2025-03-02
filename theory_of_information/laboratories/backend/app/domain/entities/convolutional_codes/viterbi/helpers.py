def hamming_distance(a, b):
    """ Returns Hamming distance of two codes """
    ones = 0  # number of 1s in xorred value (equals to HD)
    xorred = a ^ b
    while(xorred):
        ones += xorred & 1
        xorred >>= 1
    return ones

def parity(number):
    """ xors all bits in number and returns the result """
    par = 0  # inicialize to even parity
    while number:
        par ^= number & 1
        number >>= 1
    return par

# Least significant bit in polynomial matches new bit (comming into window)
# Parity computed with first polynomial in the list will be stored in most significant bit of the resulting parity bitstream
def conv_parity(window, polynomials):
    """ Calculates and returns window parity bitstream according to given list of polynomials """
    par_bits = (parity(window & pol) for pol in polynomials)  # select only bits that are significant for given polynomial
    code = 0
    for bit in par_bits:
        code = (code << 1) | bit
    return code

def bits_count(number):
    """ Returns minimum number of bit digits required to store the number. """
    i = 0
    while (1 << i) <= number:
        i += 1
    return i or 1


from Crypto.Util.randpool import RandomPool
import binascii

rp = RandomPool()

def random_byte(size):
    """
    Generate random length byte data

    @type size: integer
    @param size: size of byte data
    """
    return rp.get_bytes(size)

def random_hex(size):
    b=random_byte(size/2)
    return binascii.b2a_hex(b)

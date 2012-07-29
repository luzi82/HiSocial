from Crypto.Cipher import AES
from Crypto.Util.randpool import RandomPool
import base64
import binascii
import hashlib
import hmac
import pickle
import zlib
from hicommon import random

HASH_SALT_LENGTH = 8
HASH_SPLIT = "#"
KEY_SIZE = 32
HMAC_SIZE = 4

def gen_hash(data, hmac_value, salt=None):
    """
    Create salt+hash string from password
    Can be verified by _check_password_hash
    
    @type data: str
    @param data: The data to hash

    @type hmac_value: str
    @param hmac_value: hmac value
    
    @type salt: str
    @param salt: Salt value.  If None, this func will generate by random
    
    @rtype: str
    @return: hash value in SALT#base64(HASH) format
    """
    if(salt == None):
        salt = random.random_ascii(HASH_SALT_LENGTH)
    h = hmac.new(hmac_value, salt, hashlib.sha256)
    h.update(data)
    return salt + HASH_SPLIT + base64.b64encode(h.digest())

def check_hash(data, hmac_str, hash_value):
    """
    To check if the data match the hash
    
    @type data: str
    @param data: The password to check

    @type hmac_str: str
    @param hmac_str: hmac value
    
    @type hash_value: str
    @param hash_value: The hash value to check, in SALT#base64(HASH) format
    
    @rtype: boolean
    @return: True iff match
    """
    v = hash_value.split(HASH_SPLIT)
    if(len(v) != 2):
        return False
    vv = gen_hash(data, hmac_str, v[0])
    return vv == hash_value

def encrypt(data, key_hex):
    '''
    @param data: any obj to be pickle.dumps
    
    @type key_hex: str
    @param key_hex: key in hex format
    
    @rtype: str
    @return: encrypted data in base64
    '''
    block_size = AES.block_size
    
    if(len(key_hex) != KEY_SIZE):return None
    
    # create hmackey
    
    hmackey = random.random_byte(HMAC_SIZE)

    # Create raw data
    dump = pickle.dumps(data, 2)
    dump_hash = hmac.new(key=hmackey, msg=dump , digestmod=hashlib.md5).digest()
    vdump = dump_hash + dump
    vdumpz = zlib.compress(vdump)
    
    # add padding
    while(len(vdumpz) % block_size):
        vdumpz += '\0'
    
    iv = random.random_byte(block_size)
    key = binascii.a2b_hex(key_hex)
    
    aes = AES.new(key, AES.MODE_CBC, iv)
    enc = aes.encrypt(vdumpz)

    return base64.b64encode(hmackey + iv + enc)

def decrypt(enc_data_b64, key_hex):
    '''
    @type enc_data_b64: str
    @param enc_data_b64: encrypted data in base64
    
    @type key_hex: str
    @param key_hex: key in hex format
    
    @return: encrypted object
    '''
    block_size = AES.block_size

    if(len(key_hex) != KEY_SIZE):raise AssertionError()

    hmac_iv_enc = base64.b64decode(enc_data_b64)
    if(len(hmac_iv_enc) < HMAC_SIZE+block_size):return None

    offset = 0
    hmackey = hmac_iv_enc[offset:offset+HMAC_SIZE]
    offset += HMAC_SIZE
    iv = hmac_iv_enc[offset:offset+block_size]
    offset += block_size
    enc = hmac_iv_enc[offset:]
    
    if(len(enc) % block_size):return None
    
    key = binascii.a2b_hex(key_hex)
    
    aes = AES.new(key, AES.MODE_CBC, iv)
    vdumpz = aes.decrypt(enc)
    try: vdump = zlib.decompress(vdumpz)
    except zlib.error: return None
    
    dump_hash = vdump[0:16]
    dump = vdump[16:]
    check_hash = hmac.new(key=hmackey, msg=dump , digestmod=hashlib.md5).digest()
    if(check_hash != dump_hash):
        return None
    return pickle.loads(dump)
    
rp = RandomPool()

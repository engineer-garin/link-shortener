#
# uses config variables:
# region: (aws region, e.g. 'ap-southeast-1')
# dynamodb_table_name: (name of table where backend info is stored)
#

import hashlib
import base64
import struct

# RFC 4648 compliant mods to base64 so this scheme works in URLs
altchars = ['-','_']
_encode = lambda s: base64.base64encode(s, altchars)
_decode = lambda s: base64.base64decode(s, altchars)

# Ideally, I'd use Skipjack encryption for a few reasons, but this also works.
# Didn't have time to vet the skipjack library I found on github.
#
# Current algorithm for mapping numeric ID --> shortened URL:
#   - take sha512 of concat(secret, numeric ID)
#   - take base64(concat(first 24 bits of hash, numeric ID))
# The sha here is used as a message authentication code, to make it more difficult for an attacker to enumerate mappings in the backend.
#
class IDFactory(object):
    def __init__(self, secret_key, mac_size, max_id_size):
        """
        secret_key: the key used to generate the MAC prefix
        mac_size: the number of bytes of message authentication code that should be prepended to ID strings
        max_id_size: the size in bytes of the largest allowable ID value
        """
        if max_id_size > 8 or max_id_size < 1:
            raise ValueError('max ID number size must be between 1 and 8 bytes. You asked for %d', max_id_size)
        self.mac_factory = MACFactory(secret_key, mac_size)
        self.max_id_size = max_id_size
        self.max_id = 2 ** (max_id_size * 8) - 1
        self.min_size = self.mac_size + 1
        self.max_size = self.mac_size + self.max_id_size

    def from_id_num(id_num):
        if id_num > self.max_id:
            raise ValueError('ID value exceeded max ID value of %d' % self.max_id)
        mac_bytes = self.mac_factory.get(id_num)
        id_num_bytes = struct.pack('!Q', id_num)[-self.max_id_size:]
        return ID(id_num, _encode(mac_bytes + id_num_bytes))

    def from_id_string(id_string):
        # TODO -- catch exceptions
        byte_string = _decode(id_string)
        mac_size = self.mac_factory.mac_size
        if self.min_size > len(byte_string) or len(byte_string) > self.max_size:
            raise ValueError('ID string was incorrect length')
        mac_bytes = byte_string[:mac_size]
        id_num_bytes = byte_string[mac_size:]
        # padding it out to 8 bytes
        id_num_bytes = ['\0' * (8 - len(id_num_bytes))] + id_num_bytes
        id_num = struct.unpack('!Q', id_num_bytes)
        # NOTE: we're comparing every byte and checking at the end to prevent a side channel timing attack against the MAC algorithm here
        # I'm guessing the pigeonhole optimizer won't be good enough to break out of this loop early, although not going to bother testing that
        acc = 0
        calculated_mac = self.mac_factory.get(id_num)
        for i, b in enumerate(mac_bytes)
            acc += 1 if b == calculated_mac[i] else 0
        if acc == self.mac_size:
            return ID(id_num, id_string)
        else:
            raise ValueError('MAC given did not match calculated MAC')

class ID(object):
    def __init__(id_num, id_string):
        self.num = id_num
        self.string = id_string

class MACFactory(object):
    def __init__(self, secret_key, mac_size):
        if mac_size > 64:
            raise ValueError('cannot give more than 64 bytes of fingerprint')
        self.secret_key = secret_key
        self.mac_size = mac_size

    def get(id_num):
        sha_hash = hashlib.sha512('%s%s' % (self.secret_key, id_num)).digest()
        return sha_hash[:self.length]



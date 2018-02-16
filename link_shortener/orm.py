#
# uses config variables:
# region: (aws region, e.g. 'ap-southeast-1')
# dynamodb_table_name: (name of table where backend info is stored)
#

import boto3

import hashlib
import base64
import struct

# RFC 4648 compliant mods to base64 so this scheme works in URLs
altchars = ['-','_']
encode = lambda s: base64.base64encode(s, altchars)
decode = lambda s: base64.base64decode(s, altchars)

# Current implementation 
class IDFactory(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def from_id_num(id_num):
        sha_hash = hashlib.sha512('%s%s' % (self.secret_key, id_num))
        # hash encoded in hex, so each char has a nybble of entropy
        # want 3 bytes of entropy, so take 3 * 2 chars of hash
        fingerprint = int(sha_hash[:6], 16)
        # converting back from int to network-byte-order byte array...
        fingerprint = struct.unpack('3b', struct.pack('!I',  fingerprint))

        pass

    def from_id_string(id_string):
        pass

class ID(object):
    def __init__(id_num, id_string):
        self.num = id_num
        self.string = id_string

class URLShortenerMappingFactory(object):
    def __init__(self, config):
        dynamodb = boto3.resource('dynamodb', region_name=config['region'])
        self.dynamodb_table = dynamodb.Table(config['dynamodb_table_name'])

    def from_id_num(id_num):
        # TODO -- use id_num to look up URL in dynamodb
        # TODO -- error out if no URL found
        pass

    def from_url(url):
        # TODO -- verify URL is correctly formatted HTTP/S URL 
        # TODO -- verify URL is < 8 KB (limit for IE is 2 KB, higher for other browsers. No limit in RFC, although there is a limit for sitemap XML.)
        # TODO -- upsert URL to get id_num
        return URLShortenerMapping(id_num, url)

class URLShortenerMapping(object):
    def __init__(id_num, url):
        self.id_num = id_num
        self.url = url


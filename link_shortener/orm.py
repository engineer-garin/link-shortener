#
# uses config variables:
# region: (aws region, e.g. 'ap-southeast-1')
# dynamodb_table_name: (name of table where backend info is stored)
#

import boto3

class URLShortenerMappingFactory(object):
    def __init__(self, config):
        dynamodb = boto3.resource('dynamodb', region_name=config['region'])
        self.dynamodb_table = dynamodb.Table(config['dynamodb_table_name'])

    def from_short_id(short_id):
        # TODO -- verify short ID is in correct format
        # TODO -- convert short_id to integer
        # TODO -- use short_id to look up URL in dynamodb
        # TODO -- error out if no URL found
        pass

    def from_url(url):
        # TODO -- verify URL is correctly formatted HTTP/S URL 
        # TODO -- verify URL is < 8 KB (limit for IE is 2 KB, higher for other browsers. No limit in RFC, although there is a limit for sitemap XML.)
        # TODO -- upsert URL to get short_id
        return URLShortenerMapping(short_id, url)

class URLShortenerMapping(object):
    def __init__(short_id, url):
        self.short_id = short_id
        self.url = url


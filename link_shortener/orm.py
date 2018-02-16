
import boto3

class URLShortenerMappingFactory(object):
    def __init__(self, region_name, dynamodb_table_name):
        dynamodb = boto3.resource('dynamodb', region_name=aws_region)
        self.dynamodb_table = dynamodb.Table(dynamodb_table_name)

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


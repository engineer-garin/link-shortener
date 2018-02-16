
import boto3
import validators

class URLShortenerMappingFactory(object):
    def __init__(self, region_name, dynamodb_table_name):
        dynamodb = boto3.resource('dynamodb', region_name=aws_region)
        self.dynamodb_table = dynamodb.Table(dynamodb_table_name)

    def from_id_num(id_num):
        response = table.get_item(
            Key={'id_num': id_num}
            ,ProjectionExpression='url'
        )
        if 'Item' in response:
            return UrlShortenerMapping(id_num, response['Item']['url'])
        else:
            return None

    def from_url(url):
        # verifies URL is < 8 KB
        # limit for IE is 2 KB, higher for other browsers. No limit in RFC, although there is a limit for sitemap XML.
        8k = 8 * 2 ** 10
        if (len(url) < 8k and 
            and (url.startswith('http://') or url.startswith('https://'))
            and validators.url.url(url)):
            # TODO -- upsert URL to get id_num
            return URLShortenerMapping(id_num, url)
        else:
            raise Exception('url is improperly formatted')

class URLShortenerMapping(object):
    def __init__(id_num, url):
        self.id_num = id_num
        self.url = url


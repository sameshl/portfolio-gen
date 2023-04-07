import json
from jinja2 import Template, Markup
import boto3


bucketname = "userportfolios"
cdn = "d2c1dleky96i4z"

def lambda_handler(event, context):
    data = json.loads(event['body'])['data']
    for i in data['education']:
        i['summary'] = Markup(i['summary'])
    fobj = open('template_{}.html'.format(data['template_no']))
    template = Template(fobj.read())
    html_cv = template.render(data=data)
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketname)
    key = data['social']['email'].replace("@", "-").replace(".", "-") + ".html"
    bucket.put_object(Body=html_cv, Key=key, ACL="public-read", ContentType="text/html")

    web_page_url = "https://{}.cloudfront.net/{}".format(cdn, key)
    return {
        'statusCode': 200,
        'body': json.dumps({"message":"Successfully Generated CV!", "url": web_page_url})
    }

import json
import requests
import logging
import pprint
import boto3
from datetime import datetime, timedelta
from mail import sendmail


log = logging.getLogger("COVID")


def covid(event, context):
    resp = requests.get(
        'https://data.ontario.ca/api/3/action/datastore_search?resource_id=8b6d22e2-7065-4b0f-966f-02640be366f2&limit=50&filters={"reported_date":"2020-10-16T00:00:00","school_board":"Peel District School Board"}'
    )
    body = resp.json()

    log.info(body)
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration


def notify(event, context):
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('school-covid19-notify')

    response = table.scan()
    data_items = response['Items']

    for item in data_items:
        resp = requests.get(
            'https://data.ontario.ca/api/3/action/datastore_search?resource_id=8b6d22e2-7065-4b0f-966f-02640be366f2'
            '&limit=800'
            '&filters={"school_board":"Peel District School Board","reported_date":"%s", "school":"%s"}'
            % (yesterday, item["school"])
        )
        if resp.json()["result"]["records"]:
            sendmail(item["email"], item["school"])

# if __name__ == "__main__":
#     # pprint.pprint(covid({}, {}))
#


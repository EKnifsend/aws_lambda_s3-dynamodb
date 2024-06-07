import json
import boto3
import os


def lambda_handler(event, context):
    # TODO implement
    bucket_name = os.environ["BUCKET_NAME"]

    s3 = boto3.client("s3")
    dynamodb = boto3.resource("dynamodb")

    # Write to S3
    s3.put_object(
        Bucket=bucket_name, Key="hello.txt", Body="Hello to S3 from Lambda CDK"
    )

    # Write to DynamoDB
    table = dynamodb.Table("test-table")

    item = {"id": "1", "sortKey": 1, "message": "Hello to DynamoDB from Lambda CDK"}

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps(
            'Hello from Lambda CDK, written to test-bucket and test-table under the "Name" attribute'
        ),
    }

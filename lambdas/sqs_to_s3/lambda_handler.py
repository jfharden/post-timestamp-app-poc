import boto3
import json
import os

from sqs_to_s3.sqs_to_s3 import SQSToS3


def lambda_handler(event, context):
    boto3_session = boto3.Session()

    s3_bucket = os.environ["S3_BUCKET"]

    sqs_to_s3 = SQSToS3(boto3_session.client("s3"), s3_bucket)
    sqs_to_s3.deliver(event, context)

    return

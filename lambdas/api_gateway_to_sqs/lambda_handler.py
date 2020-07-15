import boto3
import os

from sqs_poster.sqs_poster import SQSPoster


def lambda_handler(event, context):
    boto3_session = boto3.Session()

    sqs_queue = os.environ["SQS_QUEUE"]

    sqs_poster = SQSPoster(boto3_session.client("sqs"), sqs_queue)
    sqs_poster.post(event, context)

    return

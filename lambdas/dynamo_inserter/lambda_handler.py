import boto3
import os

from dynamo_inserter.dynamo_inserter import DynamoInserter


def lambda_handler(event, context):
    boto3_session = boto3.Session()

    dynamo_table = os.environ["DYNAMO_TABLE"]

    dynamo_inserter = DynamoInserter(boto3_session.client("dynamodb"), dynamo_table)
    dynamo_inserter.insert(event, context)

    return

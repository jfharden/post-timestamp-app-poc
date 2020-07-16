import json
import time


class FailedToInsertAllItemsException(Exception):
    """Represents failure to insert everything into dynamo
    """
    pass


class DynamoInserter:
    """Accepts sqs events and writes the items into dynamo
    """
    def __init__(self, dynamo_client, dynamo_table, retry_times=None):
        """Initialise

        Args:
            dynamo_client (boto3.DynamoDB.Client): Boto3 DyanmoDB Client
            dynamo_table (string): Name of the dyanmodb table to insert to

        Keyword Args:
            retry_times (list): List of sleep times when retrying dynamo insertion. Default [5, 20, 60]
        """
        self._dynamo_client = dynamo_client
        self._dynamo_table = dynamo_table

        # Avoiding python default mutable args gotcha
        if retry_times is None:
            self._retry_times = [5, 20, 60]
        else:
            self._retry_times = retry_times

    def insert(self, event, context):
        """Insert the records received from SQS into DynamoDB

        Args:
            event (dict): Event JSON as delivered by SQS
            context (LambdaContext): Request Context as provided by SQS

        Returns:
            list of dicts: A list of every response received from dynamo

        Note: I haven't dealt with the case where we try and insert an item that
            already exists. This will raise a botocore.exceptions.ClientError with
            an error code of ConditionalCheckFailedException. In this circumstance we
            should fall back to doing individual PutItems so we can find which one it
            is, verify it's in dynamo, and discard it if it is. Without doing this we
            are breaking the idempotency of this insert, which makes me sad, but this is
            a POC (on a limited time).
        """
        request_items = {
            self._dynamo_table: self.__create_request_items(event["Records"])
        }

        responses = []

        for retry_duration in self._retry_times:
            response = self._dynamo_client.batch_write_item(RequestItems=request_items)
            responses.append(response)

            if len(response["UnprocessedItems"]) == 0:
                return responses

            request_items = response["UnprocessedItems"]

            time.sleep(retry_duration)

        response = self._dynamo_client.batch_write_item(RequestItems=request_items)
        responses.append(response)

        if len(response["UnprocessedItems"]) == 0:
            return responses

        raise FailedToInsertAllItemsException(
            "Failed items are {}".format(
                json.dumps(response["UnprocessedItems"])
            )
        )

    def __create_request_items(self, records):
        return [self.__item_put_request(record) for record in records]

    def __item_put_request(self, record):
        record_body = json.loads(record["body"])
        return {
            "PutRequest": {
                "Item": {
                    "Timestamp": {"S": record_body["timestamp"]},
                    "RequestId": {"S": record_body["request_id"]},
                }
            }
        }

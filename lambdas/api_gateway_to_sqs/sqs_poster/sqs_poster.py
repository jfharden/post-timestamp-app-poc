import json

from datetime import datetime, timezone


class SQSPoster:
    """Accepts api gateway events and writes a message to an SQS queue.

    The message is of the form:
        {
            "timestamp": <current timestamp>,
            "request_id": <api_gateway_request_id,
        }
    """
    def __init__(self, sqs_client, sqs_queue):
        """Initialise

        Args:
            sqs_client (boto3.S3.Client): Boto3 SQS Client
            sqs_queue (string): URL of the sqs queue to post to
        """
        self._sqs_client = sqs_client
        self._sqs_queue = sqs_queue

    def post(self, event, context):
        """Post a message to the SQS queue

        Args:
            event (dict): Event JSON as delivered by SQS
            context (LambdaContext): Request Context as provided by SQS

        Returns:
            dict: The sqs send_message response
        """
        sqs_message = json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": event["requestContext"]["requestId"],
        })

        return self._sqs_client.send_message(
            QueueUrl=self._sqs_queue,
            MessageBody=sqs_message,
        )

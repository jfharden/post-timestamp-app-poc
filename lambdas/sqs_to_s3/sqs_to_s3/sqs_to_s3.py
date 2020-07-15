import hashlib
import json

from base64 import b64encode
from datetime import datetime, timezone


class SQSToS3:
    """Accepts sqs events and writes the messages as files to s3
    """
    def __init__(self, s3_client, s3_bucket):
        """Initialise

        Args:
            s3_client (boto3.S3.Client): Boto3 S3 Client
            s3_bucket (string): Name of the s3 bucket to deliver to

        Returns:
            None
        """
        self._s3_client = s3_client
        self._s3_bucket = s3_bucket

    def deliver(self, event, context):
        """Deliver the records contained withtin the event to S3

        Args:
            event (dict): Event JSON as delivered by SQS
            context (LambdaContext): Request Context as provided by SQS

        Returns:
            dict: The s3 PutObject response
        """
        # Ignoring encoding errors since we know we are dealing with a bad message, and that could be
        # corrupted encoding
        event_bytes = json.dumps(event).encode("utf-8", errors="ignore")
        md5_digest = hashlib.md5(event_bytes).digest()
        event_md5sum = b64encode(md5_digest).decode("utf-8")

        # Not using isoformat time so we get more compatible filenames on s3
        s3_key = "{timestamp}_{request_id}.json".format(
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ"),
            request_id=context.aws_request_id,
        )

        return self._s3_client.put_object(
            Bucket=self._s3_bucket,
            Key=s3_key,
            Body=event_bytes,
            ContentMD5=event_md5sum,
        )

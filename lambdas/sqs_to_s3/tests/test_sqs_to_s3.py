import boto3
import datetime
import json
import os
import unittest

from botocore.stub import Stubber
from sqs_to_s3.sqs_to_s3 import SQSToS3
from unittest.mock import patch, Mock, PropertyMock


class TestSQSToS3(unittest.TestCase):
    def setUp(self):
        self._s3 = boto3.Session().client("s3")
        self._sqs_to_s3 = SQSToS3(self._s3, "bucket-foo")

    @patch("sqs_to_s3.sqs_to_s3.datetime", autospec=True)
    def test_deliver(self, mock_datetime):
        stubber = Stubber(self._s3)
        expected_body_bytes, lambda_event = self._load_sqs_message()

        timestamp = datetime.datetime.now(datetime.timezone.utc)
        stringified_time = timestamp.strftime("%Y-%m-%dT%H-%M-%SZ")
        mock_datetime.now.return_value = timestamp

        expected_params = {
            "Bucket": "bucket-foo",
            "Key": "{}_baz-request-id.json".format(stringified_time),
            "Body": expected_body_bytes,
            "ContentMD5": "nZRmuUrxb7wSbM6llcyL5A==",
        }

        s3_response = {
            "ETag": '"6805f2cfc46c0f04559748bb039d69ae"',
            "SSEKMSKeyId": "1234-21314-421414134",
        }

        stubber.add_response("put_object", s3_response, expected_params)

        with stubber:
            response = self._sqs_to_s3.deliver(lambda_event, self._context_mock())
            self.assertDictEqual(response, s3_response)

    def _context_mock(self):
        contextMock = Mock()
        type(contextMock).aws_request_id = PropertyMock(return_value="baz-request-id")

        return contextMock

    def _load_sqs_message(self):
        dirname = os.path.dirname(__file__)

        with open(os.path.join(dirname, "fixtures", "sqs_message.json"), "rb") as message:
            message_bytes = message.read()
            return message_bytes, json.loads(message_bytes.decode("utf-8"))

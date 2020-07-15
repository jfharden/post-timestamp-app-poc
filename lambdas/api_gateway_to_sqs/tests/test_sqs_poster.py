import boto3
import datetime
import json
import os
import unittest

from botocore.stub import Stubber
from sqs_poster.sqs_poster import SQSPoster
from unittest.mock import patch, Mock


class TestSQSPoster(unittest.TestCase):
    def setUp(self):
        self._sqs = boto3.Session().client("sqs")
        self._sqs_poster = SQSPoster(self._sqs, "queue-foo")

    @patch("sqs_poster.sqs_poster.datetime", autospec=True)
    def test_post(self, mock_datetime):
        stubber = Stubber(self._sqs)

        timestamp = datetime.datetime.now(datetime.timezone.utc)
        stringified_time = timestamp.isoformat()
        mock_datetime.now.return_value = timestamp

        expected_params = {
            "QueueUrl": "queue-foo",
            "MessageBody": json.dumps(
                {
                    "timestamp": stringified_time,
                    "request_id": "request-id-bar",
                }
            )
        }

        sqs_response = {
            'MD5OfMessageBody': 'string',
            'MD5OfMessageAttributes': 'string',
            'MD5OfMessageSystemAttributes': 'string',
            'MessageId': 'string',
            'SequenceNumber': 'string'
        }

        stubber.add_response("send_message", sqs_response, expected_params)

        with stubber:
            response = self._sqs_poster.post(self._load_api_gateway_event(), Mock())
            self.assertDictEqual(response, sqs_response)

    def _load_api_gateway_event(self):
        dirname = os.path.dirname(__file__)

        with open(os.path.join(dirname, "fixtures", "api_gateway_event.json")) as message:
            return json.loads(message.read())

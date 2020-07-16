import boto3
import datetime
import json
import os
import unittest

from botocore.stub import Stubber
from dynamo_inserter.dynamo_inserter import DynamoInserter, FailedToInsertAllItemsException
from unittest.mock import Mock


class TestDynamoInserter(unittest.TestCase):
    def setUp(self):
        self._dynamodb = boto3.Session().client("dynamodb")
        self._dynamo_inserter = DynamoInserter(self._dynamodb, "table-foo", retry_times=[0.1])
        self._stubber = Stubber(self._dynamodb)
        self._initial_expected_params = {
            "RequestItems": {
                "table-foo": [
                    {
                        "PutRequest": {
                            "Item": {
                                "Timestamp": {"S": "2020-07-15T15:18:08+00:00"},
                                "RequestId": {"S": "Root=1-5759e988-bd862e3fe1be46a994272793"},
                            }
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "Timestamp": {"S": "2020-07-27T10:00:00+01:00"},
                                "RequestId": {"S": "Root=1-12434235c-ab3223353245"},
                            }
                        }
                    },
                ]
            }
        }

    def test_insert(self):
        dynamo_response = {
            "UnprocessedItems": {}
        }

        self._stubber.add_response("batch_write_item", dynamo_response, self._initial_expected_params)

        with self._stubber:
            response = self._dynamo_inserter.insert(self._load_sqs_message(), Mock())
            self.assertEqual(response, [dynamo_response])

    def test_insert_with_unprocessed_items(self):
        dynamo_response = {
            "UnprocessedItems": {
                "table-foo": [
                    {
                        "PutRequest": {
                            "Item": {
                                "Timestamp": {"S": "2020-07-27T10:00:00+01:00"},
                                "RequestId": {"S": "Root=1-12434235c-ab3223353245"},
                            }
                        }
                    },
                ]
            }
        }

        expected_retry_params = {
            "RequestItems": {
                "table-foo": [
                    {
                        "PutRequest": {
                            "Item": {
                                "Timestamp": {"S": "2020-07-27T10:00:00+01:00"},
                                "RequestId": {"S": "Root=1-12434235c-ab3223353245"},
                            }
                        }
                    },
                ]
            }
        }

        dynamo_retry_response = {
            "UnprocessedItems": {}
        }

        self._stubber.add_response("batch_write_item", dynamo_response, self._initial_expected_params)
        self._stubber.add_response("batch_write_item", dynamo_retry_response, expected_retry_params)

        with self._stubber:
            response = self._dynamo_inserter.insert(self._load_sqs_message(), Mock())
            self.assertEqual(response, [dynamo_response, dynamo_retry_response])

    def test_insert_with_failure_to_insert_all_items(self):
        dynamo_response = {
            "UnprocessedItems": {
                "table-foo": [
                    {
                        "PutRequest": {
                            "Item": {
                                "Timestamp": {"S": "2020-07-27T10:00:00+01:00"},
                                "RequestId": {"S": "Root=1-12434235c-ab3223353245"},
                            }
                        }
                    },
                ]
            }
        }

        expected_retry_params = {
            "RequestItems": {
                "table-foo": [
                    {
                        "PutRequest": {
                            "Item": {
                                "Timestamp": {"S": "2020-07-27T10:00:00+01:00"},
                                "RequestId": {"S": "Root=1-12434235c-ab3223353245"},
                            }
                        }
                    },
                ]
            }
        }

        self._stubber.add_response("batch_write_item", dynamo_response, self._initial_expected_params)
        self._stubber.add_response("batch_write_item", dynamo_response, expected_retry_params)

        with self._stubber:
            with self.assertRaises(FailedToInsertAllItemsException):
                self._dynamo_inserter.insert(self._load_sqs_message(), Mock())

    def _load_sqs_message(self):
        dirname = os.path.dirname(__file__)

        with open(os.path.join(dirname, "fixtures", "sqs_message.json")) as message:
            return json.loads(message.read())

import os
import json
import unittest

import requests
from mock import Mock, patch
import broker


class TestBroker(unittest.TestCase):
    def setUp(self):
        self.client = broker.app.test_client()

    def test_index(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        content_type = response.headers.get("Content-type")
        self.assertEqual(content_type, "application/json")

        parsed_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(parsed_response, {"ok": "yes"})

    def test_catalog(self):
        response = self.client.get("/v2/catalog")

        self.assertEqual(response.status_code, 200)

        content_type = response.headers.get("Content-type")
        self.assertEqual(content_type, "application/json")

        parsed_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(parsed_response["services"][0]["id"], "e76a6581-7e8e-4c3d-9e11-906ee5109c77")
        self.assertEqual(parsed_response["services"][0]["plans"][0]["id"], "7b16c0ff-5e1a-4081-b40d-8ffc1106a385")

    def test_provision(self):
        response = self.client.put("/v2/service_instances/e40892dd-8656-49f6-a456-d8c997ce6a40")

        self.assertEqual(response.status_code, 200)

        content_type = response.headers.get("Content-type")
        self.assertEqual(content_type, "application/json")

    @patch('requests.put')
    def test_bind(self, mock_requests_put):
        os.environ["TOKEN"] = "token_here"
        os.environ["CREDHUB_SERVER"] = "credhub_server_url"

        credhub_response = Mock(requests.Response)
        credhub_response.status_code = 200
        mock_requests_put.return_value = credhub_response

        response = self.client.put(
            "/v2/service_instances/e40892dd-8656-49f6-a456-d8c997ce6a40/service_bindings/3cdee985-a3f7-4d30-8502-8392cced69a7")

        self.assertEqual(response.status_code, 200)

        content_type = response.headers.get("Content-type")
        self.assertEqual(content_type, "application/json")

        credhubkey = "/c/example-broker-client/credhub-example-service/f95ddffd-f9b2-4694-9d3d-85c311c69fcc/cred2"

        parsed_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(parsed_response["credentials"]["key"], credhubkey)

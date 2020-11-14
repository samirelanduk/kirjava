import json
from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from kirjava import Client

class ClientCreationTests(TestCase):

    def test_can_create_client(self):
        client = Client("http://url")
        self.assertEqual(client._url, "http://url")
        self.assertEqual(client._headers, {
         "Accept": "application/json", "Content-Type": "application/json"
        })



class ClientReprTests(TestCase):

    def test_client_repr(self):
        client = Client("http://url")
        self.assertEqual(repr(client), "<Client (URL: http://url)>")



class ClientUrlTests(TestCase):

    def test_can_get_client_url(self):
        client = Client("http://url")
        self.assertIs(client._url, client.url)



class ClientHeaderTests(TestCase):

    def test_can_get_client_headers(self):
        client = Client("http://url")
        self.assertIs(client._headers, client.headers)



class ClientHistoryTests(TestCase):

    def test_can_get_client_history(self):
        client = Client("http://url")
        client._history = [1, 2]
        self.assertEqual(client.history, (1, 2))



class ClientExecutionTests(TestCase):

    def test_can_send_query(self):
        client = Client("http://url")
        client.session = Mock()
        result = client.execute("MESSAGE")
        client.session.request.assert_called_with(
            "POST", "http://url", headers=client._headers, data='{"query": "MESSAGE"}'
        )
        self.assertEqual(result, client.session.request.return_value.json.return_value)
        self.assertEqual(client._history, [(
            {"string": "MESSAGE", "variables": {}},
            client.session.request.return_value.json.return_value
        )])


    def test_can_send_query_with_different_verb(self):
        client = Client("http://url")
        client.session = Mock()
        result = client.execute("MESSAGE", method="GET")
        client.session.request.assert_called_with(
            "GET", "http://url", headers=client._headers, data='{"query": "MESSAGE"}'
        )
        self.assertEqual(result, client.session.request.return_value.json.return_value)


    def test_can_send_query_with_variables(self):
        client = Client("http://url")
        client.session = Mock()
        result = client.execute("MESSAGE", variables={"S": "T"})
        client.session.request.assert_called_with(
         "POST", "http://url", headers=client._headers, data='{"query": "MESSAGE", "variables": {"S": "T"}}'
        )
        self.assertEqual(result, client.session.request.return_value.json.return_value)
        self.assertEqual(client._history, [(
         {"string": "MESSAGE", "variables": {"S": "T"}},
         client.session.request.return_value.json.return_value
        )])
    

    def test_can_handle_non_json_response(self):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.return_value.json.side_effect = json.decoder.JSONDecodeError("", "", 0)
        client.session.request.return_value.headers = {"Content-type": "text/html"}
        client.session.request.return_value.content = b"<html></html>"
        with self.assertRaises(ValueError) as e:
            result = client.execute("MESSAGE")
        self.assertEqual(
            str(e.exception),
            "Server did not return JSON, it returned text/html:\n<html></html>"
        )
    

    def test_can_handle_non_json_response_too_long(self):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.return_value.json.side_effect = json.decoder.JSONDecodeError("", "", 0)
        client.session.request.return_value.headers = {"Content-type": "text/html"}
        client.session.request.return_value.content = b"<html></html>" * 100
        with self.assertRaises(ValueError) as e:
            result = client.execute("MESSAGE")
        self.assertEqual(
            str(e.exception), "Server did not return JSON, it returned text/html"
        )
    

    def test_can_handle_non_json_response_binary(self):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.return_value.json.side_effect = json.decoder.JSONDecodeError("", "", 0)
        client.session.request.return_value.headers = {"Content-type": "image/png"}
        client.session.request.return_value.content = b"\xf8\xee"
        with self.assertRaises(ValueError) as e:
            result = client.execute("MESSAGE")
        self.assertEqual(
            str(e.exception), "Server did not return JSON, it returned image/png"
        )
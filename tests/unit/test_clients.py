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



class ClientExecutionTests(TestCase):

    @patch("requests.request")
    def test_can_send_query(self, mock_request):
        client = Client("http://url")
        result = client.execute("MESSAGE")
        mock_request.assert_called_with(
         "POST", "http://url", headers=client._headers, data='{"query": "MESSAGE"}'
        )
        self.assertEqual(result, mock_request.return_value.json.return_value)


    @patch("requests.request")
    def test_can_send_query_with_different_verb(self, mock_request):
        client = Client("http://url")
        result = client.execute("MESSAGE", method="GET")
        mock_request.assert_called_with(
         "GET", "http://url", headers=client._headers, data='{"query": "MESSAGE"}'
        )
        self.assertEqual(result, mock_request.return_value.json.return_value)


    @patch("requests.request")
    def test_can_send_query_with_variables(self, mock_request):
        client = Client("http://url")
        result = client.execute("MESSAGE", variables={"S": "T"})
        mock_request.assert_called_with(
         "POST", "http://url", headers=client._headers, data='{"query": "MESSAGE", "variables": {"S": "T"}}'
        )
        self.assertEqual(result, mock_request.return_value.json.return_value)

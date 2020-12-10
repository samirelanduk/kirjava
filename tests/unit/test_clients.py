import json
import io
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

    def setUp(self):
        self.patch1 = patch("kirjava.client.get_files_from_variables")
        self.patch2 = patch("kirjava.client.create_response_error_message")
        self.mock_files = self.patch1.start()
        self.mock_error = self.patch2.start()
        self.mock_files.return_value = (None, None)
    

    def tearDown(self):
        self.patch1.stop()
        self.patch2.stop()

    def test_can_send_query(self):
        client = Client("http://url")
        client.session = Mock()
        result = client.execute("MESSAGE")
        self.mock_files.assert_called_with(None)
        client.session.request.assert_called_with(
            "POST", "http://url", headers=client._headers,
            data='{"variables": null, "query": "MESSAGE"}'
        )
        self.assertEqual(result, client.session.request.return_value.json.return_value)
        self.assertEqual(client._history, [(
            {"query": "MESSAGE", "variables": {}},
            client.session.request.return_value.json.return_value
        )])


    def test_can_send_query_with_different_verb(self):
        client = Client("http://url")
        client.session = Mock()
        result = client.execute("MESSAGE", method="GET")
        client.session.request.assert_called_with(
            "GET", "http://url", headers=client._headers,
            data='{"variables": null, "query": "MESSAGE"}'
        )
        self.assertEqual(result, client.session.request.return_value.json.return_value)


    def test_can_send_query_with_variables(self):
        client = Client("http://url")
        client.session = Mock()
        self.mock_files.return_value = ({"S": "T"}, None)
        result = client.execute("MESSAGE", variables={"S": "T"})
        self.mock_files.assert_called_with({"S": "T"})
        client.session.request.assert_called_with(
            "POST", "http://url", headers=client._headers, data='{"variables": {"S": "T"}, "query": "MESSAGE"}'
        )
        self.assertEqual(result, client.session.request.return_value.json.return_value)
        self.assertEqual(client._history, [(
            {"query": "MESSAGE", "variables": {"S": "T"}},
            client.session.request.return_value.json.return_value
        )])
    

    @patch("mimetypes.MimeTypes")
    def test_can_send_query_with_files(self, mock_mime):
        client = Client("http://url")
        client.session = Mock()
        self.mock_files.return_value = ({"S": "T"}, {"file1": None, "file2": None})
        file1, file2 = Mock(), Mock()
        file1.name, file2.name = "f1name", "f2name"
        mock_mime.return_value.guess_type.return_value = ["filename"]
        self.mock_files.return_value = ({"S": "T"}, {"file1": file1, "file2": file2})
        result = client.execute("MESSAGE", variables={"S": "T"})
        self.mock_files.assert_called_with({"S": "T"})
        client.session.request.assert_called_with(
            "POST", "http://url",
            files={
                "0": ("f1name", file1.read.return_value, "filename"),
                "1": ("f2name", file2.read.return_value, "filename"),
            }, 
            data={
                "operations": '{"variables": {"S": "T"}, "query": "MESSAGE"}',
                "map": '{"0": ["variables.file1"], "1": ["variables.file2"]}'
            },
            headers={'Accept': "application/json"},
        )
        self.assertEqual(result, client.session.request.return_value.json.return_value)
        self.assertEqual(client._history, [(
            {"query": "MESSAGE", "variables": {"S": "T"}},
            client.session.request.return_value.json.return_value
        )])
    

    def test_can_handle_non_json_response(self):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.return_value.json.side_effect = json.decoder.JSONDecodeError("", "", 0)
        with self.assertRaises(ValueError) as e:
            result = client.execute("MESSAGE")
        self.mock_error.assert_called_with(client.session.request.return_value)
        self.assertEqual(
            str(e.exception),
            str(self.mock_error.return_value)
        )
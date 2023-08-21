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
        self.patch2 = patch("kirjava.client.files_to_map")
        self.patch3 = patch("kirjava.client.pack_files")
        self.patch4 = patch("kirjava.client.create_response_error_message")
        self.patch5 = patch("kirjava.client.Client.request_with_retries")
        self.mock_files = self.patch1.start()
        self.mock_map = self.patch2.start()
        self.mock_pack = self.patch3.start()
        self.mock_error = self.patch4.start()
        self.mock_request = self.patch5.start()
        self.mock_map.return_value = {"0": ["MAP"]}
        self.mock_pack.return_value = {"0": ["packed"]}
        self.mock_files.return_value = (None, None)
    

    def tearDown(self):
        self.patch1.stop()
        self.patch2.stop()
        self.patch3.stop()
        self.patch4.stop()
        self.patch5.stop()


    def test_can_send_query(self):
        client = Client("http://url")
        client.session = Mock()
        result = client.execute("MESSAGE")
        self.mock_files.assert_called_with(None)
        self.mock_request.assert_called_with(
            operation='{"variables": null, "query": "MESSAGE"}',
            headers=client._headers, method="POST", retries=0, retry_statuses=None
        )
        self.assertEqual(result, self.mock_request.return_value.json.return_value)
        self.assertEqual(client._history, [(
            {"query": "MESSAGE", "variables": {}},
            self.mock_request.return_value.json.return_value
        )])
    

    def test_can_send_query_with_retries(self):
        client = Client("http://url")
        client.session = Mock()
        result = client.execute("MESSAGE", retries=3, retry_statuses=[1, 2])
        self.mock_files.assert_called_with(None)
        self.mock_request.assert_called_with(
            operation='{"variables": null, "query": "MESSAGE"}',
            headers=client._headers, method="POST", retries=3, retry_statuses=[1, 2]
        )
        self.assertEqual(result, self.mock_request.return_value.json.return_value)
        self.assertEqual(client._history, [(
            {"query": "MESSAGE", "variables": {}},
            self.mock_request.return_value.json.return_value
        )])


    def test_can_send_query_with_different_verb(self):
        client = Client("http://url")
        client.session = Mock()
        result = client.execute("MESSAGE", method="GET")
        self.mock_request.assert_called_with(
            operation='{"variables": null, "query": "MESSAGE"}',
            headers=client._headers, method="GET", retries=0, retry_statuses=None
        )
        self.assertEqual(result, self.mock_request.return_value.json.return_value)


    def test_can_send_query_with_variables(self):
        client = Client("http://url")
        client.session = Mock()
        self.mock_files.return_value = ({"S": "T"}, None)
        result = client.execute("MESSAGE", variables={"S": "T"})
        self.mock_files.assert_called_with({"S": "T"})
        self.mock_request.assert_called_with(
            operation='{"variables": {"S": "T"}, "query": "MESSAGE"}',
            headers=client._headers, method="POST", retries=0, retry_statuses=None
        )
        self.assertEqual(result, self.mock_request.return_value.json.return_value)
        self.assertEqual(client._history, [(
            {"query": "MESSAGE", "variables": {"S": "T"}},
            self.mock_request.return_value.json.return_value
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
        self.mock_request.assert_called_with(
            method="POST", retries=0, retry_statuses=None,
            files={"0": ["packed"]}, 
            operation={
                "operations": '{"variables": {"S": "T"}, "query": "MESSAGE"}',
                "map": '{"0": ["MAP"]}'
            },
            headers={'Accept': "application/json"},
        )
        self.assertEqual(result, self.mock_request.return_value.json.return_value)
        self.assertEqual(client._history, [(
            {"query": "MESSAGE", "variables": {"S": "T"}},
            self.mock_request.return_value.json.return_value
        )])
    

    def test_can_handle_non_json_response(self):
        client = Client("http://url")
        client.session = Mock()
        self.mock_request.return_value.json.side_effect = json.decoder.JSONDecodeError("", "", 0)
        with self.assertRaises(ValueError) as e:
            client.execute("MESSAGE")
        self.mock_error.assert_called_with(self.mock_request.return_value)
        self.assertEqual(
            str(e.exception),
            str(self.mock_error.return_value)
        )



class ClientRetryTests(TestCase):

    def test_simple_request_without_retries(self):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.return_value.status_code = 500
        resp = client.request_with_retries(
            operation="operation", headers="headers", method="method", files="files"
        )
        self.assertEqual(resp, client.session.request.return_value)
        client.session.request.assert_called_with(
            "method", "http://url", data="operation", headers="headers", files="files"
        )
    

    def test_zero_retry_allows_failure(self):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.side_effect = Exception()
        with self.assertRaises(Exception):
            client.request_with_retries(
                operation="operation", headers="headers", method="method", files="files"
            )
        self.assertEqual(client.session.request.call_count, 1)
    

    @patch("time.sleep")
    def test_can_retry(self, mock_sleep):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.side_effect = [Exception, Exception, Exception, "RESP"]
        resp = client.request_with_retries(
            operation="operation", headers="headers", method="method", files="files", retries=5
        )
        self.assertEqual(resp, "RESP")
        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(4)
        mock_sleep.assert_any_call(8)
        self.assertEqual(client.session.request.call_count, 4)
    

    @patch("time.sleep")
    def test_can_retry_to_limit(self, mock_sleep):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.side_effect = [Exception, Exception, Exception, "RESP"]
        with self.assertRaises(Exception):
            client.request_with_retries(
                operation="operation", headers="headers", method="method", files="files", retries=2
            )
        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(4)
        self.assertEqual(client.session.request.call_count, 3)
    

    def test_simple_request_without_retries(self):
        client = Client("http://url")
        client.session = Mock()
        resp = client.request_with_retries(
            operation="operation", headers="headers", method="method", files="files"
        )
        self.assertEqual(resp, client.session.request.return_value)
        client.session.request.assert_called_with(
            "method", "http://url", data="operation", headers="headers", files="files"
        )
    

    def test_can_fail_on_status_code(self):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.return_value.status_code = 500
        with self.assertRaises(Exception):
            client.request_with_retries(
                operation="operation", headers="headers", method="method", files="files", retry_statuses=[500]
            )
        client.session.request.assert_called_with(
            "method", "http://url", data="operation", headers="headers", files="files"
        )
    

    @patch("time.sleep")
    def test_can_retry_on_status_code(self, mock_sleep):
        client = Client("http://url")
        client.session = Mock()
        client.session.request.return_value.status_code = 500
        with self.assertRaises(Exception):
            client.request_with_retries(
                operation="operation", headers="headers", method="method", files="files", retry_statuses=[500], retries=5
            )
        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(4)
        mock_sleep.assert_any_call(8)
        mock_sleep.assert_any_call(16)
        mock_sleep.assert_any_call(32)
        self.assertEqual(client.session.request.call_count, 6)
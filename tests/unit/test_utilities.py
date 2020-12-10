import io
from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from kirjava.utilities import *

class ExecutionTests(TestCase):

    @patch("kirjava.client.Client")
    def test_can_quick_execute(self, mock_client):
        response = execute("http://url", 1, a=2)
        mock_client.assert_called_with("http://url")
        mock_client.return_value.execute.assert_called_with(1, a=2)
        self.assertIs(response, mock_client.return_value.execute.return_value)


    @patch("kirjava.client.Client")
    def test_can_quick_execute_with_headers(self, mock_client):
        response = execute("http://url", 1, headers={"x": 4, "y": 5}, a=2)
        mock_client.assert_called_with("http://url")
        mock_client.return_value.headers.update.assert_called_with({"x": 4, "y": 5})
        mock_client.return_value.execute.assert_called_with(1, a=2)
        self.assertIs(response, mock_client.return_value.execute.return_value)



class FilesFromVariablesTests(TestCase):

    def test_can_handle_no_variables(self):
        self.assertEqual(get_files_from_variables(None), (None, None))
    

    def test_can_handle_variables_without_files(self):
        self.assertEqual(get_files_from_variables({1: 2, 3: 4}), ({1: 2, 3: 4}, {}))
    

    def test_can_handle_variables_with_files(self):
        f = io.IOBase()
        self.assertEqual(
            get_files_from_variables({1: 2, 3: 4, 5: f}),
            ({1: 2, 3: 4, 5: None}, {5: f})
        )



class ResponseErrorMessageTests(TestCase):

    def test_binary_response_error(self):
        response = Mock(headers={"Content-type": "bin"}, content=r"\x00\x02")
        self.assertEqual(
            create_response_error_message(response),
            "Server did not return JSON, it returned bin"
        )
    

    def test_short_string_response_error(self):
        response = Mock(headers={"Content-type": "str"}, content=b"12345678")
        self.assertEqual(
            create_response_error_message(response),
            "Server did not return JSON, it returned str:\n12345678"
        )
    

    def test_long_string_response_error(self):
        response = Mock(headers={"Content-type": "str"}, content=b"12" * 1000)
        self.assertEqual(
            create_response_error_message(response),
            "Server did not return JSON, it returned str"
        )

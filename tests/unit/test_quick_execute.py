from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from kirjava import execute

class ExecutionTests(TestCase):

    @patch("kirjava.Client")
    def test_can_quick_execute(self, mock_client):
        response = execute("http://url", 1, a=2)
        mock_client.assert_called_with("http://url")
        mock_client.return_value.execute.assert_called_with(1, a=2)
        self.assertIs(response, mock_client.return_value.execute.return_value)


    @patch("kirjava.Client")
    def test_can_quick_execute_with_headers(self, mock_client):
        response = execute("http://url", 1, headers={"x": 4, "y": 5}, a=2)
        mock_client.assert_called_with("http://url")
        mock_client.return_value.headers.update.assert_called_with({"x": 4, "y": 5})
        mock_client.return_value.execute.assert_called_with(1, a=2)
        self.assertIs(response, mock_client.return_value.execute.return_value)

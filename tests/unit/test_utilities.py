import io
from unittest import TestCase
from unittest.mock import Mock, patch
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
    

    def test_can_handle_variables_with_lists_files(self):
        f1 = io.IOBase()
        f2 = io.IOBase()
        self.assertEqual(
            get_files_from_variables({1: 2, 3: 4, 5: [f1, f2]}),
            ({1: 2, 3: 4, 5: [None, None]}, {5: [f1, f2]})
        )



class FilesToMapTests(TestCase):

    def test_can_convert_single_files_to_map(self):
        files = {"image1": "x", "image2": "y"}
        map = files_to_map(files)
        self.assertEqual(map, {"0": ["variables.image1"], "1": ["variables.image2"]})
    

    def test_can_convert_multi_files_to_map(self):
        files = {"image1": "x", "images": ["1", "2"], "image2": "y"}
        map = files_to_map(files)
        self.assertEqual(map, {
            "0": ["variables.image1"],
            "1": ["variables.images.0"],
            "2": ["variables.images.1"],
            "3": ["variables.image2"],
        })



class FilePackingTests(TestCase):

    def test_can_pack_single_files(self):
        f1 = Mock()
        f2 = Mock()
        f1.name = "file1.txt"
        f2.name = "file2.txt"
        files = {"image1": f1, "image2": f2}
        packed_files = pack_files(files)
        self.assertEqual(packed_files, {
            "0": ("file1.txt", f1.read.return_value, "text/plain"),
            "1": ("file2.txt", f2.read.return_value, "text/plain"),
        })
    

    def test_can_pack_multiple_files(self):
        f1 = Mock()
        f2 = Mock()
        f3 = Mock()
        f4 = Mock()
        f1.name = "file1.txt"
        f2.name = "file2.txt"
        f3.name = "file3.txt"
        f4.name = "file4.txt"
        files = {"image1": f1, "images": [f2, f3], "image2": f4}
        packed_files = pack_files(files)
        self.assertEqual(packed_files, {
            "0": ("file1.txt", f1.read.return_value, "text/plain"),
            "1": ("file2.txt", f2.read.return_value, "text/plain"),
            "2": ("file3.txt", f3.read.return_value, "text/plain"),
            "3": ("file4.txt", f4.read.return_value, "text/plain"),
        })



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

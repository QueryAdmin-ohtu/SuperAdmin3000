import unittest
from unittest.mock import Mock, patch, mock_open
import os

from logger.logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.filename = "logfile.log"
        self.logger = Logger("testuser", self.filename)

        self.request = Mock()
        setattr(self.request, "method", "POST")
        setattr(self.request, "path", "/testpath")
        setattr(self.request, "form", {"csrf_token": "SECRET",
                                       "public_field": "publicdata",
                                       "fieldB": "bb"})

    @patch("builtins.open", mock_open(read_data="""[EVENT] 31-12-2099 15:55:55 This is an example event 
[ERROR] 02-02-2100 11:11:11 This is a second example event"""))
    def test_read_all_events_returns_text(self):
        result = self.logger.read_all_events()

        open.assert_called_with(self.filename, "r")
            
        self.assertEqual(len(result), 2)
        self.assertTrue("example" in result[0])
        self.assertTrue("ERROR" in result[1])

    @patch("builtins.open", mock_open(read_data="first line\n   second, indented line\nthird_line"))
    def test_read_all_events_indented_lines_are_appended_to_the_string(self):
        result = self.logger.read_all_events()

        self.assertEqual(len(result), 2)        

        self.assertTrue("first" in result[0])
        self.assertTrue("second" in result[0])
        self.assertTrue("third" in result[1])
        

    @patch("builtins.open")
    def test_read_all_events_handles_wrong_filename(self, m):
        m.side_effect = IOError

        result = self.logger.read_all_events()

        open.assert_called_with(self.filename, "r")

        self.assertIsNone(result)

    @patch("builtins.open")
    def test_log_post_request_adds_log_entry(self, m):

        result = self.logger.log_post_request(self.request)

        self.assertTrue("public" in result)
        self.assertFalse("SECRET" in result)

        open.assert_called_once_with(self.filename, "a")
        # TODO: fix this
        # open.write.assert_called_once_with(result)

    @patch("builtins.open")
    def test_write_adds_log_entry(self, m):
        result = self.logger.write("This is a test02")

        self.assertTrue("test02" in result)

        open.assert_called_once_with(self.filename, "a")
        # TODO: fix this
        # open.write.assert_called_once_with(result)

    @patch("os.remove")
    def test_delete_log_deletes_file(self, m):

        result = self.logger._delete_log()

        self.assertTrue(result)
        m.assert_called_once_with(self.filename)

    @patch("os.remove")
    def test_delete_log_handles_bad_filename(self, m):
        m.side_effect = IOError

        result = self.logger._delete_log()

        self.assertFalse(result)
        m.assert_called_once_with(self.filename)

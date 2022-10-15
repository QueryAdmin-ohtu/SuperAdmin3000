import unittest
from unittest.mock import patch, mock_open

from logger.logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.filename = "logfile.log"
        self.logger = Logger("testuser", self.filename)

    @patch("builtins.open", mock_open(read_data="""[EVENT] 31-12-2099 15:55:55 This is an example event 
[ERROR] 02-02-2100 11:11:11 This is a second example event"""))
    def test_get_all_events_returns_text(self):
        result = self.logger.read_all_events()

        self.assertEqual(len(result), 2)
        self.assertTrue("example" in result[0])
        self.assertTrue("ERROR" in result[1])
        
        open.assert_called_with(self.filename, "r")
        
    @patch("builtins.open")
    def test_log_event_adds_log_entry(self, m):
        result = self.logger.write("This is a test02")

        self.assertTrue("test02" in result)

        open.assert_called_once_with(self.filename, "a")
        # TODO: fix this
        # open.write.assert_called_once_with(result)
        

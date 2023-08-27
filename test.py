import unittest
import abs_mdbook_transfer


class Test_transfer(unittest.TestCase):
    def test_format_print(self):
        self.assertLogs(abs_mdbook_transfer.format_print("ERROR", "Error msg"))
        self.assertLogs(abs_mdbook_transfer.format_print('WARN', "Warning msg"))
        self.assertLogs(abs_mdbook_transfer.format_print('INFO', "Info msg"))


if __name__ == '__main__':
    unittest.main()
    
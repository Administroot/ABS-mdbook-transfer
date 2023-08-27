import unittest
import abs_mdbook_transfer


class Test_transfer(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.summary = abs_mdbook_transfer.mdfile(abs_mdbook_transfer.MDPATH + "SUMMARY.md")
        super().__init__(methodName)

    def test_format_print(self):
        self.assertLogs(abs_mdbook_transfer.format_print("ERROR", "Error msg"))
        self.assertLogs(abs_mdbook_transfer.format_print('WARN', "Warning msg"))
        self.assertLogs(abs_mdbook_transfer.format_print('INFO', "Info msg"))

    def test_summary(self):
        self.assertLogs(abs_mdbook_transfer.update_summary(self.summary))

    def test_transform(self):
        self.assertLogs(abs_mdbook_transfer.transform(abs_mdbook_transfer.MDPATH))


if __name__ == '__main__':
    unittest.main()
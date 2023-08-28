import unittest
import abs_mdbook_transfer

TEST_SUM_CTX = "\n## 测试\n* [test-hint](test/transfer-hint.md)"


class Test_transfer(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.mdfile_class = abs_mdbook_transfer.mdfile(abs_mdbook_transfer.MDPATH + "SUMMARY.md")
        try:
            self.include_test_dir()
        except Exception:
            abs_mdbook_transfer.format_print("ERROR", "Test suite init failed!")
            exit(2)

    # Include test dir
    def include_test_dir(self) -> None:
        abs_mdbook_transfer.cp_files({"test": "src/test"})
        # Append test content
        self.append(TEST_SUM_CTX)

    def append(self, content: str) -> None:
        try:
            with open(self.mdfile_class.file_path, "a", encoding='utf-8') as fp:
                if self.mdfile_class.file_ctx.find("test-hint") == -1:
                    fp.write(content)
        except Exception:
            abs_mdbook_transfer.format_print("WARN", f"{self.mdfile_class.file_path}已存在。")

    def test_format_print(self):
        self.assertLogs(abs_mdbook_transfer.format_print("ERROR", "Error msg"))
        self.assertLogs(abs_mdbook_transfer.format_print('WARN', "Warning msg"))
        self.assertLogs(abs_mdbook_transfer.format_print('INFO', "Info msg"))

    def test_mdfile_class(self):
        self.assertLogs(abs_mdbook_transfer.update_summary(self.mdfile_class))

    # def test_transform(self):
    #     self.assertLogs(abs_mdbook_transfer.transform(abs_mdbook_transfer.MDPATH))

    def test_partial_replacement(self):
        self.mdfile_class = abs_mdbook_transfer.mdfile(abs_mdbook_transfer.MDPATH + "test/transfer-hint.md")
        abs_mdbook_transfer.format_print("INFO", "TESTING FILE: " + self.mdfile_class.file_path)
        self.assertLogs(self.mdfile_class.partial_replacement())


if __name__ == '__main__':
    unittest.main()
import unittest
from generatesite import extract_title

class TestGenerateSite(unittest.TestCase):
    def test_title(self):
        md = """
    # Hello

    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        title = extract_title(md)
        self.assertEqual(title, "Hello")

    def test_no_title(self):
        md = """
    ## Hello

    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        title = extract_title(md)
        self.assertRaisesRegex(ValueError, "There is no h1 element")
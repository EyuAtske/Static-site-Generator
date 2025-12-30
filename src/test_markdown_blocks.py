import unittest
from markdown_blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        def test_markdown_to_blocks_execces_lines(self):
            md = """
                    This is **bolded** paragraph



                    This is another paragraph with _italic_ text and `code` here
                    This is the same paragraph on a new line



                    - This is a list
                    - with items
                """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        def test_block_to_block_type(self):
            self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
            self.assertEqual(block_to_block_type("``` \ncode block\n```"), BlockType.CODE)
            self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
            self.assertEqual(block_to_block_type("- List item 1"), BlockType.UNORDERED_LIST)
            self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
            self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)
        def test_block_to_block_type_multiple_order(self):
            self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
            self.assertEqual(block_to_block_type("``` \ncode block\n```"), BlockType.CODE)
            self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
            self.assertEqual(block_to_block_type("- List item 1"), BlockType.UNORDERED_LIST)
            self.assertEqual(block_to_block_type("1. First item\n2. Second item\n3. Third item"), BlockType.ORDERED_LIST)
            self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)
        def test_block_to_block_type_noorder(self):
            self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
            self.assertEqual(block_to_block_type("``` \ncode block\n```"), BlockType.CODE)
            self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
            self.assertEqual(block_to_block_type("- List item 1"), BlockType.UNORDERED_LIST)
            self.assertEqual(block_to_block_type("1. First item\n3. second item\n and bla bla bla"), BlockType.PARAGRAPH)
            self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)
        def test_block_to_block_type_incorrect_unordered(self):
            self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
            self.assertEqual(block_to_block_type("``` \ncode block\n```"), BlockType.CODE)
            self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
            self.assertEqual(block_to_block_type("-List item 1"), BlockType.PARAGRAPH)
            self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
            self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)
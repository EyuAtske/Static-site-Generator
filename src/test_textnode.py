import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)
    def test_instance(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsInstance(node, TextNode)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_image(self):
        node = TextNode("i", TextType.IMAGE,"https:google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {
            "src": node.url,
            "alt": node.text
        })
    def test_split_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    def test_split_node_nested(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a `Italic block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("Italic block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    def test_split_node_invalid(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertRaisesRegex(IndexError, "There is no closing delimiter")
    def test_split_both_delimiters(self):
        node = TextNode("This is text with a **code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertRaisesRegex(IndexError, "There is no closing delimiter")
    def test_split_invalid_delimiters(self):
        node = TextNode("This is text with a *code block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.CODE)
        self.assertRaisesRegex(ValueError, "Incorrect delimiter")
    def test_split_bold_node(self):
        node = TextNode("This is **code block** text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        print(new_nodes)
        self.assertEqual(new_nodes,[
            TextNode("This is ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])


if __name__ == "__main__":
    unittest.main()
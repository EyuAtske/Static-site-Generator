import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1")
        node2 = HTMLNode("h1")
        self.assertEqual(node, node2)
    def test_propeq(self):
        dist = {
            "href" : "http",
            "link": "home"
        }
        node = HTMLNode("a", "link to home", None, dist)
        returned = node.props_to_html()
        self.assertEqual(
            " href=http link=home", returned
        )
    def test_rerpeq(self):
        node = HTMLNode("a", "link to home")
        self.assertEqual(
            "HTMLNode (a, link to home, None, None)", repr(node)
        )
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p> Hello, world! </p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a  href=https://www.google.com> Click me! </a>")

    def test_leaf_exception(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        self.assertRaisesRegex(ValueError, "All leaf nodes must have a value")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "None", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "None")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span> child </span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b> grandchild </b></span></div>",
        )
    def test_to_html_multiple_children(self):
        child_node = LeafNode("span", "child")
        grandchild_node = LeafNode("b", "grandchild")
        parent_node = ParentNode("div", [child_node, grandchild_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span> child </span><b> grandchild </b></div>",
        )
    def test_to_html_nested_parent(self):
        child_node = LeafNode("span", "child")
        grandchild_node = LeafNode("b", "grandchild")
        grand_parent_node = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("div", [child_node, grand_parent_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span> child </span><div><b> grandchild </b></div></div>",
        )

import unittest

from markdown_tohtml import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b> bolded </b> paragraph text in a p tag here</p><p>This is another paragraph with <i> italic </i> text and <code> code </code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code> This is text that _should_ remain\nthe **same** even with inline stuff </code></pre></div>",
        )
    def test_unordered_list(self):
        md = """
    - This is text that _should_ remain
    - the **same** even with inline stuff
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is text that <i> should </i> remain</li><li>the <b> same </b> even with inline stuff</li></ul></div>",
        )
    def test_ordered_list(self):
        md = """
    1. This is text that _should_ remain
    2. the **same** even with inline stuff
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is text that <i> should </i> remain</li><li>the <b> same </b> even with inline stuff</li></ol></div>",
        )
    def test_Heading(self):
        md = """
    # Heading 1

    ## Heading 2

    ### Heading 3

    #### Heading 4

    ##### Heading 5

    ###### Heading 6
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )
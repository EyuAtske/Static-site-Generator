from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from main import text_to_textnodes, text_node_to_html_node
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    print(len(blocks))
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            html_node = HTMLNode("p", block)
            parent_node = ParentNode(f"p", text_to_children(block)).to_html()
            block_nodes.extend(text_to_children(parent_node))
        elif block_type == BlockType.HEADING:
            txt = block.split(" ")
            level = len(txt[0])
            content = " ".join(txt[1:])
            html_node = HTMLNode(f"h{level}", content)
            parent_node = ParentNode(f"h{level}", text_to_children(content)).to_html()
            block_nodes.extend(text_to_children(parent_node))
        elif block_type == BlockType.CODE:
            text = block.split("\n")
            text.pop()
            text.pop(0)
            code_content = "\n".join(text)
            html_node = HTMLNode("code", code_content)
            node = TextNode(code_content, TextType.CODE)
            html_node.children = text_node_to_html_node(node)
            parent = ParentNode("pre", [text_node_to_html_node(node)]).to_html()
            node2 = TextNode(parent, TextType.TEXT)
            block_nodes.extend([text_node_to_html_node(node2)])
        elif block_type == BlockType.QUOTE:
            txt = block.split(" ")
            quote_content = " ".join(txt[1:])
            html_node = HTMLNode("blockquote", quote_content)
            block_nodes.extend(text_to_children(block))
        elif block_type == BlockType.UNORDERED_LIST:
            lists = block.split("\n")
            ul_node = HTMLNode("ul", None)
            parents = []
            for l in lists:
                list_content = l[2:]
                html_node = HTMLNode("li", list_content)
                html_node.children = text_to_children(list_content)
                parent = ParentNode("li", html_node.children)
                parents.append(parent)
            ul_node.children = parents
            grand_parent_node = ParentNode("ul", ul_node.children).to_html()
            block_nodes.extend(text_to_children(grand_parent_node))
        elif block_type == BlockType.ORDERED_LIST:
            lists = block.split("\n")
            ol_node = HTMLNode("ol", None)
            parents = []
            for l in lists:
                list_content = l[3:]
                html_node = HTMLNode("li", list_content)
                html_node.children = text_to_children(list_content)
                parent = ParentNode("li", html_node.children)
                parents.append(parent)
            ol_node.children = parents
            grand_parent_node = ParentNode("ol", ol_node.children).to_html()
            block_nodes.extend(text_to_children(grand_parent_node))
    parent_node = ParentNode("div", block_nodes)
    print(parent_node.to_html())
    return parent_node
def text_to_children(text):
    node = text_to_textnodes(text)
    nodes = []
    for t in node:
        nodes.append(text_node_to_html_node(t))
    return nodes
def parent_to_children(parent_node):
    parent_node.children = text_to_children(parent_node.value)
    parent = ParentNode(parent_node.tag, parent_node.children)
    return parent.to_html()
import re
from textnode import TextType, TextNode
class HTMLNode():
    def __init__(self, tag=None, value=None,children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("Not implemented")
    def props_to_html(self):
        if not self.props:
            return ""
        prop_string = ""
        for key in self.props.keys():
            prop_string = prop_string  + " " + key + "=" +  self.props[key]
        return prop_string
    def __repr__(self):
        return f"HTMLNode ({self.tag}, {self.value}, {self.children}, {self.props})"
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag is None:
            return self.value
        if self.props is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        elif self.children is None:
            raise ValueError("All parent nodes must have children")
        parent_str = f"<{self.tag}>"
        for child in self.children:
            parent_str += child.to_html()
        parent_str += f"</{self.tag}>"
        return parent_str

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_textNodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_textNodes.append(old)
        else:
            chr = list(old.text)
            inline = []
            type_text = []
            queue = []
            c = 0
            if chr[c] == delimiter:
                print(True, old.text)
            try:
                while c < len(chr):
                    if text_type == TextType.BOLD:
                        deli = chr[c] + chr[c+1]
                        if deli == delimiter:
                            c += 2
                            if len(type_text) > 0:
                                if "".join(type_text) != "":
                                    queue.append(("".join(type_text), TextType.TEXT))
                                    type_text = []
                            deli = chr[c] + chr[c+1]
                            while deli != delimiter:
                                inline.append(chr[c])
                                c += 1
                                deli = chr[c] + chr[c+1]
                            c += 1
                            queue.append(("".join(inline).strip(), text_type))
                            print(inline, text_type)
                            inline = []
                        else:
                            if c == len(chr)-2:
                                type_text.append(chr[c])
                                type_text.append(chr[c+1])
                            else:
                                type_text.append(chr[c])
                    elif chr[c] == delimiter:
                        if len(type_text) > 0:
                            if "".join(type_text) != "":
                                queue.append(("".join(type_text), TextType.TEXT))
                                type_text = []
                        c += 1
                        while chr[c] != delimiter:
                            inline.append(chr[c])
                            c += 1
                        c += 1
                        queue.append(("".join(inline).strip(), text_type))
                        print(inline, text_type)
                        inline = []
                    else:
                        type_text.append(chr[c])
                    c += 1
            except IndexError as i:
                print("There is no closing delimiter")
            if "".join(type_text) != "":
                queue.append(("".join(type_text), TextType.TEXT))
            for q in queue:
                new_textNodes.append(TextNode(q[0], q[1]))
    return new_textNodes
def extract_markdown_images(text):
    matches = []
    alt_matches = re.findall(r"\!\[(.*?)\]", text)
    src_matches = re.findall(r"\((.*?)\)", text)
    for i in range(len(alt_matches)):
        matches.append((alt_matches[i], src_matches[i]))
    return matches

def extract_markdown_links(text):
    matches = []
    alt_matches = re.findall(r"(?<!!)\[(.*?)\]", text)
    link_matches = re.findall(r"\((.*?)\)", text)
    for i in range(len(alt_matches)):
        matches.append((alt_matches[i], link_matches[i]))
    return matches
def split_nodes_image(old_nodes):
    new_nodes = []
    for old in old_nodes:
        if old.text_type == TextType.TEXT:
            images = extract_markdown_images(old.text)
            if len(images) == 0:
                new_nodes.append(old)
            else:
                temp_text = old.text
                for img in images:
                    parts = temp_text.split(f"![{img[0]}]({img[1]})", 1)
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
                    if parts[1]:
                        temp_text = parts[1]
                    else:
                        temp_text = ""
                if temp_text:
                    new_nodes.append(TextNode(temp_text, TextType.TEXT))
        else:
            new_nodes.append(old)
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for old in old_nodes:
        if old.text_type == TextType.TEXT:
            links = extract_markdown_links(old.text)
            if len(links) == 0:
                new_nodes.append(old)
            else:
                temp_text = old.text
                for link in links:
                    parts = temp_text.split(f"[{link[0]}]({link[1]})", 1)
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    if len(parts) > 1:
                        temp_text = parts[1]
                    else:
                        temp_text = ""
                if temp_text:
                    new_nodes.append(TextNode(temp_text, TextType.TEXT))
        else:
            new_nodes.append(old)
    return new_nodes
def text_node_to_html_node(text_node):
    if text_node is None:
        raise ValueError("There is no text node")
    else:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text )
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        elif text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {
                "src": text_node.url,
                "alt": text_node.text
            })
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
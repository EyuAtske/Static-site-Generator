from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node is None:
        raise ValueError("There is no text node")
    else:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        elif text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode("i", None, {
                "src": text_node.url,
                "alt": text_node.text
            })
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_textNodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_textNodes.append(old)
        else:
            type_delimiter = ""
            try:
                if delimiter == "`":
                    type_delimiter = "code"
                elif delimiter == "_":
                    type_delimiter = "italic"
                elif delimiter == "**":
                    type_delimiter = "bold"
            except ValueError as v:
                print ("Incorrect delimiter")
            chr = list(old.text)
            inline = []
            type_text = []
            queue = []
            c = 0
            try:
                while c < len(chr):
                    if type_delimiter == "bold":
                        deli = chr[c] + chr[c+1]
                        if deli == delimiter:
                            c += 2
                            if len(type_text) == 0:
                                continue
                            else:
                                queue.append(("".join(type_text), "text"))
                                type_text = []
                            deli = chr[c] + chr[c+1]
                            while deli != delimiter:
                                inline.append(chr[c])
                                c += 1
                                deli = chr[c] + chr[c+1]
                            c += 1
                            queue.append(("".join(inline), type_delimiter))
                            inline = []
                        else:
                            if c == len(chr)-2:
                                type_text.append(chr[c])
                                type_text.append(chr[c+1])
                            else:
                                type_text.append(chr[c])
                    elif chr[c] == delimiter:
                        if len(type_text) == 0:
                            continue
                        else:
                            queue.append(("".join(type_text), "text"))
                            type_text = []
                        c += 1
                        while chr[c] != delimiter:
                            inline.append(chr[c])
                            c += 1
                        queue.append(("".join(inline), type_delimiter))
                    else:
                        type_text.append(chr[c])
                    c += 1
            except IndexError as i:
                print("There is no closing delimiter")
            queue.append(("".join(type_text), "text"))
            for q in queue:
                if q[1] == "bold":
                    new_textNodes.append(TextNode(q[0], TextType.BOLD))
                elif q[1] == "code":
                    new_textNodes.append(TextNode(q[0], TextType.CODE))
                elif q[1] == "italic":
                    new_textNodes.append(TextNode(q[0], TextType.ITALIC))
                else:
                    new_textNodes.append(TextNode(q[0], TextType.TEXT))
    return new_textNodes


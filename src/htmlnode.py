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
            return f"<{self.tag} {self.props_to_html()}> {self.value} </{self.tag}>"
        return f"<{self.tag}> {self.value} </{self.tag}>"

        
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
from htmlnode import HTMLNode
from functools import reduce

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag passed to Parent Node")
        if not self.children:
            raise ValueError("No children passed to Parent Node")

        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"
        return open_tag + reduce(lambda s,children: s + children.to_html(), self.children, "") + close_tag

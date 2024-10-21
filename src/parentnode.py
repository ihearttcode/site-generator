from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None) -> None:
        if children is None or children == []:
            raise ValueError("Parent nodes must have children!")
        if tag is None:
            raise ValueError("Parent nodes must have valid tags")
        
        super().__init__(tag=tag, children=children, props=props)
        
    """
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have valid tags!")
        if self.children is None or self.children == []:
            raise ValueError("Parent nodes must have children!")
        child_html = ''
        open_tag = f'<{self.tag}{super().props_to_html()}>'
        close_tag = f'</{self.tag}>'
        for child in self.children:
            child_html += child.to_html()
        return f'{open_tag}{child_html}{close_tag}'
    """
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


# Base class for text nodes
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def to_html(self):
        return self.text
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        # Get all attributes that are not methods or built-in properties
        attributes = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        return all(getattr(self, attr) == getattr(other, attr) for attr in attributes)
    def __repr__(self, printr=False):
        if printr:
            print(f"TextNode(text={self.text!r}, text_type={self.text_type!r}, url={self.url!r})")
            return
        return f"TextNode(text={self.text!r}, text_type={self.text_type!r}, url={self.url!r})"

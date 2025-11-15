from enum import Enum

class TextType(Enum):
    BOLD = 'bold'
    ITALIC = 'italic'
    UNDERLINE = 'underline'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"

    def render(self) -> str:
        if self.text_type == TextType.BOLD:
            return f"<b>{self.text}</b>"
        elif self.text_type == TextType.ITALIC:
            return f"<i>{self.text}</i>"
        elif self.text_type == TextType.UNDERLINE:
            return f"<u>{self.text}</u>"
        elif self.text_type == TextType.LINK:
            return f'<a href="{self.url}">{self.text}</a>'
        elif self.text_type == TextType.IMAGE:
            return f'<img src="{self.url}" alt="Image"/>'
        else:
            return self.text
    
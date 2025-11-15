from enum import Enum

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
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

    def text_node_to_html_node(self) -> str:
        match self.text_type:
            case TextType.TEXT:
                return self.text
            case TextType.BOLD:
                return f"<b>{self.text}</b>"
            case TextType.ITALIC:
                return f"<i>{self.text}</i>"
            case TextType.CODE:
                return f"<code>{self.text}</code>"
            case TextType.UNDERLINE:
                return f"<u>{self.text}</u>"
            case TextType.LINK:
                return f'<a href="{self.url}">{self.text}</a>'
            case TextType.IMAGE:
                return f'<img src="{self.url}" alt="Image"/>'
            case _:
                return self.text
    
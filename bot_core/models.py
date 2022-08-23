import typing as t


class SendMessage:
    def __init__(self, content: t.Optional[str] = None, image_path: t.Optional[str] = None):
        self.content = content
        self.image_path = image_path

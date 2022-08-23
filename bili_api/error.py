from typing import Optional


class BiliRequestError(Exception):
    def __init__(self, *args, modify_msg: Optional[str] = None, print_out=True, call_master=False):
        super().__init__(*args)
        self.modify_msg = modify_msg
        self.print_out = print_out
        self.call_master = call_master

    def __repr__(self):
        if self.modify_msg is not None:
            return self.modify_msg
        else:
            return super().__repr__()

    def __str__(self):
        if self.modify_msg is not None:
            return self.modify_msg
        else:
            return super().__str__()


class InvalidCookieError(Exception):
    pass

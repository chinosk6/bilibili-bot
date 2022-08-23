import bili_api
from . import models as m
from .bot_codes import BotCodes
from typing import Union


def reply_at_message(ctx: bili_api.models.AtMessageItem, data):
    send_content = ""
    if isinstance(data, m.SendMessage):
        send_content = data.content
    elif isinstance(data, str):
        send_content = data

    if send_content != "":
        print(f"发送艾特回复: {send_content}")
        return bili_api.fast_reply_at_message(ctx, send_content)

def reply_chat_message(ctx: bili_api.models.ChatSessionHistoryMessage, data):
    send_content = None
    send_image_path = None
    if isinstance(data, m.SendMessage):
        send_content = data.content
        send_image_path = data.image_path
    elif isinstance(data, str):
        send_content = data
    return bili_api.fast_reply_chat(ctx, send_content, send_image_path)


def reply_message(ctx: Union[bili_api.models.AtMessageItem, bili_api.models.ChatSessionHistoryMessage],
                  data, msg_type: int):
    if msg_type == BotCodes.AT_MESSAGE:
        return reply_at_message(ctx, data)

    if msg_type in [BotCodes.GROUP_MESSAGE, BotCodes.PRIVATE_MESSAGE]:
        return reply_chat_message(ctx, data)

from bot_core import CommandRegister, BotCodes
from bot_core.models import SendMessage
from bili_api.models import AtMessageItem, ChatSessionHistoryMessage


@CommandRegister.reg_exactly_match("nihao", allowed_type=[BotCodes.AT_MESSAGE])
def at_hello(ctx: AtMessageItem):
    print("hello", ctx.user.nickname, ctx.user.mid)
    return "Hello World!"


@CommandRegister.reg_startswith("/echo ", allowed_type=[BotCodes.PRIVATE_MESSAGE])
def chat_echo(ctx: ChatSessionHistoryMessage, ckv: str):
    # `ckv`为可选参数, 不同的注册方式会传入不同的字符串
    # reg_startswith, reg_endswith 和 reg_starts_and_endswith 会传入 去除指令部分后 的消息文本
    # reg_regex 和 reg_exactly_match 会传入消息原文本
    return ckv


@CommandRegister.reg_exactly_match("nihao", allowed_type=[BotCodes.PRIVATE_MESSAGE, BotCodes.GROUP_MESSAGE])
def chat_hello(ctx: ChatSessionHistoryMessage):
    print("hello", ctx.sender_uid)
    return "Hello World!"


@CommandRegister.reg_exactly_match("/testimg", allowed_type=[BotCodes.PRIVATE_MESSAGE, BotCodes.GROUP_MESSAGE])
def chat_hello_img(ctx: ChatSessionHistoryMessage):
    print("testimg", ctx.sender_uid)
    return SendMessage(image_path="falconlove.png")

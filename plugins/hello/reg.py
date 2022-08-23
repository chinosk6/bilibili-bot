from bot_core import CommandRegister, BotCodes
from bot_core.models import SendMessage
from bili_api.models import AtMessageItem, ChatSessionHistoryMessage


@CommandRegister.reg_exactly_match("nihao", allowed_type=[BotCodes.AT_MESSAGE])
def at_hello(ctx: AtMessageItem):
    print("hello", ctx.user.nickname, ctx.user.mid)
    return "Hello World!"

@CommandRegister.reg_exactly_match("nihao", allowed_type=[BotCodes.PRIVATE_MESSAGE, BotCodes.GROUP_MESSAGE])
def chat_hello(ctx: ChatSessionHistoryMessage):
    print("hello", ctx.sender_uid)
    return "Hello World!"


@CommandRegister.reg_exactly_match("/testimg", allowed_type=[BotCodes.PRIVATE_MESSAGE, BotCodes.GROUP_MESSAGE])
def chat_hello_img(ctx: ChatSessionHistoryMessage):
    print("testimg", ctx.sender_uid)
    return SendMessage(image_path="falconlove.png")

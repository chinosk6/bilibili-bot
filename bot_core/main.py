from threading import Thread
import time
import random
import bili_api
from .message_processor import MessageProcessor
from .bot_codes import BotCodes, regist_func_count


class BiliBot(MessageProcessor):
    def __init__(self):
        super().__init__()
        self._running = False

    def update_message_status(self):
        def _():
            if regist_func_count.get(BotCodes.AT_MESSAGE, 0) > 0:
                unread_count = bili_api.get_unread_msg_count().data
                if unread_count.at > 0:
                    self.at_message_processor()

            if regist_func_count.get(BotCodes.PRIVATE_MESSAGE, 0) > 0:
                chat_unread_count = bili_api.get_chat_unread_count().data
                if (chat_unread_count.follow_unread + chat_unread_count.unfollow_unread) > 0:
                    self.chat_message_processor()

        Thread(target=_).start()


    def run(self, sleep_base=30, offset=10):
        print(f"Bot开始运行\nAT_MESSAGE 注册数量: {regist_func_count.get(BotCodes.AT_MESSAGE, 0)}"
              f"\nPRIVATE_MESSAGE 注册数量: {regist_func_count.get(BotCodes.PRIVATE_MESSAGE, 0)}"
              f"\nGROUP_MESSAGE 注册数量: {regist_func_count.get(BotCodes.GROUP_MESSAGE, 0)}")
        if self._running:
            return
        else:
            self._running = True
        while True:
            if not self._running:
                break
            self.update_message_status()
            time.sleep(sleep_base - random.randint(0, offset * 2) + offset)

import json
import time
from threading import Thread
from .data_processor import DataProcessor
from .message_register import get_matching_methods
from .bot_codes import BotCodes
from . import api
import bili_api


class MessageProcessor(DataProcessor):
    def __init__(self):
        super().__init__()
        self.chat_start_ts = int(time.time() * 1000000)

    @staticmethod
    def do_match(ctx, msg_content, msg_type):
        def _():
            match_func = get_matching_methods(msg_content, msg_type)
            for mt_func, mt_ucmd in match_func:  # func, `ckv`
                paras = mt_func.__code__.co_varnames
                para_len = len(paras)
                args = []
                kwargs = {}
                if "ckv" in paras:
                    kwargs["ckv"] = mt_ucmd
                if "mt_ucmd" in paras:
                    kwargs["mt_ucmd"] = mt_ucmd
                if para_len >= 1:
                    args = [ctx]
                try:
                    reply_msg = mt_func(*args, **kwargs)
                    if reply_msg is not None:
                        api.reply_message(ctx, reply_msg, msg_type)
                except BaseException as e:
                    print(f"指令处理失败: {e}")  # TODO 错误处理
        Thread(target=_).start()


    def at_message_processor(self):
        data = bili_api.get_at_messages()
        unprocessed = self.at_msg_in(data)
        if not unprocessed:
            return

        for i in unprocessed:
            print(f"{i.user.nickname} 艾特消息: {i.item.source_content}")
            selfuid, selfname = bili_api.get_self_uid()  # 自身uid和昵称
            i.item.bot_message_str = i.item.source_content.replace(f"@{selfname}", "").strip()
            self.do_match(i, i.item.bot_message_str, BotCodes.AT_MESSAGE)


    def chat_message_processor(self):
        session_data = bili_api.get_chat_sessions(self.chat_start_ts).data
        if session_data.session_list is None:
            return

        max_ts = 0
        try:
            for i in session_data.session_list:
                if i.session_ts > max_ts:
                    max_ts = i.session_ts

                if i.session_type == 1:
                    msg_type = BotCodes.PRIVATE_MESSAGE  # 私聊
                elif i.session_type == 2:
                    msg_type = BotCodes.GROUP_MESSAGE  # 应援团
                else:
                    print(f"unknown session_type: {i.session_type}")
                    continue

                chat_data = bili_api.get_chat_history(i.talker_id, i.session_type)
                unprocessed = self.chat_msg_in(chat_data.data)
                for m in unprocessed:
                    selfuid, selfname = bili_api.get_self_uid()  # 自身uid和昵称
                    if m.sender_uid == selfuid:  # 过滤自身消息
                        continue
                    try:
                        msg = json.loads(m.content)
                        msg_content = msg.get("content", "").replace(f"@{selfname}", "").strip()
                        msg_img_url = msg.get("url", None)
                    except BaseException as e:
                        print(f"解析消息失败: {e}")
                        msg_content = m.content
                        msg_img_url = None

                    if msg_img_url is not None:
                        msg_content = f"{msg_content}[bot:image,url={msg_img_url}]"

                    m.content = msg_content
                    print(f"{m.sender_uid} 发送消息: {m.content}")
                    self.do_match(m, m.content, msg_type)
        finally:
            if max_ts > self.chat_start_ts:
                self.chat_start_ts = max_ts
            self.chat_start_ts += 1

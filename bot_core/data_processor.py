import sqlite3
import bili_api
from bili_api import models
from typing import List


class DataProcessor:
    def __init__(self, at_dont_process_when_offline=False, chat_dont_process_when_offline=True):
        """
        数据库处理部分
        :param at_dont_process_when_offline: 不处理离线状态下的评论区艾特消息
        :param chat_dont_process_when_offline: 不处理离线状态下的聊天消息
        """
        self.conn = sqlite3.connect("bilimsg.db", check_same_thread=False)
        self.db_init()

        self._at_reindex: bool = at_dont_process_when_offline
        self.chat_dont_process_when_offline: bool = chat_dont_process_when_offline


    def db_init(self):
        cursor = self.conn.cursor()
        tables = [i[0] for i in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        if "at_processed" not in tables:
            cursor.execute("""CREATE TABLE "at_processed" (
              "msg_id" text NOT NULL,
              "timestamp" integer NOT NULL,
              "data" text NOT NULL
            )""")
            self._at_reindex = True
        if "chat_processed" not in tables:
            cursor.execute("""CREATE TABLE "chat_processed" (
              "msg_id" text NOT NULL,
              "timestamp" integer NOT NULL,
              "data" text NOT NULL
            )""")

        self.conn.commit()


    def at_msg_in(self, data: models.AtMessages) -> List[models.AtMessageItem]:
        retdata = []
        cursor = self.conn.cursor()
        processed_data = cursor.execute(
            "SELECT msg_id, timestamp, data FROM at_processed ORDER BY timestamp DESC limit 20"
        ).fetchall()
        processed_ids = [str(i[0]) for i in processed_data]

        for i in data.data.items:
            msg_id = str(i.id)
            if msg_id not in processed_ids:
                retdata.append(i)
                cursor.execute("INSERT INTO at_processed (msg_id, timestamp, data) VALUES (?, ?, ?)",
                               [msg_id, i.at_time, i.json()])

        self.conn.commit()

        if self._at_reindex:
            self._at_reindex = False
            return []
        else:
            return retdata

    def chat_msg_in(self, data: models.ChatSessionHistoryData) -> List[models.ChatSessionHistoryMessage]:
        retdata = []
        cursor = self.conn.cursor()
        processed_data = cursor.execute(
            "SELECT msg_id, timestamp, data FROM chat_processed ORDER BY timestamp DESC limit 20"
        ).fetchall()
        processed_ids = [str(i[0]) for i in processed_data]

        for i in data.messages[::-1]:
            msg_id = str(i.msg_key)
            if msg_id not in processed_ids:

                if self.chat_dont_process_when_offline:
                    if i.timestamp >= bili_api.LOAD_TIME:
                        retdata.append(i)
                else:
                    retdata.append(i)

                cursor.execute("INSERT INTO chat_processed (msg_id, timestamp, data) VALUES (?, ?, ?)",
                               [msg_id, i.timestamp, i.json()])

        self.conn.commit()
        return retdata

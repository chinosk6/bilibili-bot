from typing import Optional, List, Any
from pydantic import BaseModel


class UnreadData(BaseModel):
    at: Optional[int]
    chat: Optional[int]
    like: Optional[int]
    reply: Optional[int]
    sys_msg: Optional[int]
    up: Optional[int]


class Unread(BaseModel):  # 未读消息数
    code: Optional[int] = None
    message: Optional[str] = None
    ttl: Optional[int] = None
    data: Optional[UnreadData] = None


class AtMessageCursor(BaseModel):
    is_end: Optional[bool]
    id: Optional[int]
    time: Optional[int]


class AtMessageUser(BaseModel):
    mid: Optional[int]
    fans: Optional[int]
    nickname: Optional[str]
    avatar: Optional[str]
    mid_link: Optional[str]
    follow: Optional[bool]


class AtDetail(BaseModel):
    mid: Optional[int]
    fans: Optional[int]
    nickname: Optional[str]
    avatar: Optional[str]
    mid_link: Optional[str]
    follow: Optional[bool]


class TopicDetail(BaseModel):
    topic_id: Optional[int]
    topic_name: Optional[str]
    is_activity: Optional[int]
    topic_link: Optional[str]


class AtMessageItemItem(BaseModel):
    type: Optional[str]
    business: Optional[str]
    business_id: Optional[int]
    title: Optional[str]
    image: Optional[str]
    uri: Optional[str]
    subject_id: Optional[int]
    root_id: Optional[int]
    target_id: Optional[int]
    source_id: Optional[int]
    source_content: Optional[str]
    native_uri: Optional[str]
    at_details: Optional[List[AtDetail]]
    topic_details: Optional[List[TopicDetail]]
    hide_reply_button: Optional[bool]
    bot_message_str: Optional[str]

    def __init__(self, **data):
        super().__init__(**data)
        self.bot_message_str: Optional[str] = data.get("source_content", "")



class AtMessageItem(BaseModel):
    id: Optional[int]
    user: Optional[AtMessageUser]
    item: Optional[AtMessageItemItem]
    at_time: Optional[int]


class AtMessageData(BaseModel):
    cursor: Optional[AtMessageCursor]
    items: Optional[List[AtMessageItem]]


class AtMessages(BaseModel):  # 艾特消息
    code: Optional[int] = None
    message: Optional[str] = None
    ttl: Optional[int] = None
    data: Optional[AtMessageData] = None

class ChatUnreadData(BaseModel):
    unfollow_unread: Optional[int]
    follow_unread: Optional[int]
    unfollow_push_msg: Optional[int]
    dustbin_push_msg: Optional[int]
    dustbin_unread: Optional[int]
    biz_msg_unfollow_unread: Optional[int]
    biz_msg_follow_unread: Optional[int]

class ChatUnreadCount(BaseModel):  # 聊天未读消息数量
    code: Optional[int] = None
    msg: Optional[str] = None
    message: Optional[str] = None
    ttl: Optional[int] = None
    data: Optional[ChatUnreadData] = None



class LastMsg(BaseModel):
    sender_uid: Optional[int]
    receiver_type: Optional[int]
    receiver_id: Optional[int]
    msg_type: Optional[int]
    content: Optional[str]
    msg_seqno: Optional[int]
    timestamp: Optional[int]
    at_uids: Optional[List[int]]
    msg_key: Optional[int]
    msg_status: Optional[int]
    notify_code: Optional[str]


class SessionListItem(BaseModel):
    talker_id: Optional[int]
    session_type: Optional[int]
    at_seqno: Optional[int]
    top_ts: Optional[int]
    group_name: Optional[str]
    group_cover: Optional[str]
    is_follow: Optional[int]
    is_dnd: Optional[int]
    ack_seqno: Optional[int]
    ack_ts: Optional[int]
    session_ts: Optional[int]
    unread_count: Optional[int]
    last_msg: Optional[LastMsg]
    group_type: Optional[int]
    can_fold: Optional[int]
    status: Optional[int]
    max_seqno: Optional[int]
    new_push_msg: Optional[int]
    setting: Optional[int]
    is_guardian: Optional[int]
    is_intercept: Optional[int]
    is_trust: Optional[int]
    system_msg_type: Optional[int]
    live_status: Optional[int]
    biz_msg_unread_count: Optional[int]
    user_label: Any  # TODO


class ChatSessionsData(BaseModel):
    session_list: Optional[List[SessionListItem]]  # 没有则为None
    has_more: Optional[int]
    anti_disturb_cleaning: Optional[bool]
    is_address_list_empty: Optional[int]
    show_level: Optional[bool]


class ChatSessions(BaseModel):  # 指定时间戳后的消息
    code: Optional[int] = None
    msg: Optional[str] = None
    message: Optional[str] = None
    ttl: Optional[int] = None
    data: Optional[ChatSessionsData] = None


class ChatSessionHistoryMessage(BaseModel):
    sender_uid: Optional[int]
    receiver_type: Optional[int]
    receiver_id: Optional[int]
    msg_type: Optional[int]
    content: Optional[str]
    msg_seqno: Optional[int]
    timestamp: Optional[int]
    at_uids: Optional[List[int]]
    msg_key: Optional[int]
    msg_status: Optional[int]
    notify_code: Optional[str]


class ChatSessionHistoryData(BaseModel):
    messages: Optional[List[ChatSessionHistoryMessage]]
    has_more: Optional[int]
    min_seqno: Optional[int]
    max_seqno: Optional[int]


class ChatSessionHistory(BaseModel):  # 消息记录
    code: Optional[int] = None
    msg: Optional[str] = None
    message: Optional[str] = None
    ttl: Optional[int] = None
    data: Optional[ChatSessionHistoryData] = None


class UploadImageData(BaseModel):
    image_url: Optional[str]
    image_width: Optional[int]
    image_height: Optional[int]


class UploadImage(BaseModel):  # 上传图片
    code: Optional[int] = None
    message: Optional[str] = None
    ttl: Optional[int] = None
    data: Optional[UploadImageData] = None


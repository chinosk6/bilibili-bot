import json
import random
import time
import imghdr
from .bili_config import BiliCfg
from . import models, error
import requests
import typing as t
from http.cookies import SimpleCookie

uid_cache = {}  # cookie: [str(uid), nickname]


def get_cookie(cookie_index: t.Optional[int] = BiliCfg.cookieIndex):
    if isinstance(BiliCfg.cookies, str):
        return BiliCfg.cookies

    if cookie_index is None:
        return BiliCfg.cookies[random.randint(0, len(BiliCfg.cookies) - 1)]
    else:
        return BiliCfg.cookies[cookie_index]


def get_gene_headers(cookie_index: t.Optional[int] = BiliCfg.cookieIndex):
    return {
        'Accept': "application/json",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
        'Cookie': get_cookie(cookie_index),
        'origin': 'https://message.bilibili.com',
        'referer': 'https://message.bilibili.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': BiliCfg.ua
    }


def return_checker(response: requests.Response, ret_models=None, valid_http_codes: t.Optional[t.List[int]] = None):
    if valid_http_codes is None:
        valid_http_codes = [200]

    if response.status_code not in valid_http_codes:
        try:
            data = json.loads(response.text)
            if "message" not in data:
                data["message"] = f"响应失败: {response.status_code}"
            if "code" not in data:
                data["code"] = response.status_code
        except:
            data = {"code": -1919810, "message": "响应失败, 格式不正确"}
        print(response.text)
        raise error.BiliRequestError(response.text, modify_msg=data.get("message", "请求失败"))
    else:
        try:
            data = json.loads(response.text)
            if "code" in data:
                if data["code"] != 0:
                    print(f"可能请求失败: {data.get('message', None)}")
        except:
            pass

        if ret_models is None:
            return response.text
        else:
            return ret_models(**json.loads(response.text))


def get_unread_msg_count() -> models.Unread:
    url = "http://api.bilibili.com/x/msgfeed/unread"
    response = requests.request("GET", url, headers=get_gene_headers())
    return return_checker(response, ret_models=models.Unread)


def get_at_messages() -> models.AtMessages:
    url = "https://api.bilibili.com/x/msgfeed/at?build=0&mobi_app=web"
    response = requests.request("GET", url, headers=get_gene_headers())
    return return_checker(response, ret_models=models.AtMessages)


def get_self_uid():
    global uid_cache

    headers = get_gene_headers()
    cookie = headers["Cookie"]
    if cookie in uid_cache:
        return uid_cache[cookie]

    url = "https://api.bilibili.com/x/space/myinfo"
    response = requests.request("GET", url, headers=headers)
    data = json.loads(return_checker(response))
    uid = data["data"]["mid"]
    unick = data["data"]["name"]
    uid_cache[cookie] = [str(uid), unick]
    return [str(uid), unick]


def get_csrf():
    csrf = SimpleCookie(get_cookie()).get("bili_jct", None)
    if csrf is None:
        raise error.InvalidCookieError(f"missing required data: bili_jct")
    return csrf.value


def reply_at_message(subject_id, message, root, parent, csrf_token, csrf) -> str:
    url = "https://api.bilibili.com/x/v2/reply/add"
    payload = {
        "oid": subject_id,
        "type": 17,
        "message": message,
        "root": root,
        "parent": parent,
        "jsonp": "jsonp",
        "scene": "msg",
        "plat": 1,
        "from": "im-reply",
        "build": 0,
        "mobi_app": "web",
        "csrf_token": csrf_token,
        "csrf": csrf
    }
    response = requests.request("POST", url, headers=get_gene_headers(), data=payload)
    return return_checker(response)


def fast_reply_at_message(ctx: models.AtMessageItem, message: str, with_reply_info=True):
    csrf = get_csrf()
    if with_reply_info:
        if ctx.item.type in ["reply"]:
            message = f"@{ctx.user.nickname} : {message}"

    return reply_at_message(ctx.item.subject_id, message, ctx.item.source_id, ctx.item.source_id, csrf, csrf)


def get_chat_unread_count() -> models.ChatUnreadCount:
    url = "https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread"
    response = requests.request("GET", url, headers=get_gene_headers())
    return return_checker(response, ret_models=models.ChatUnreadCount)


def get_chat_sessions(begin_ts: int) -> models.ChatSessions:
    """
    获取指定时间后的消息列表
    :param begin_ts: 开始时间, 16位时间戳
    """
    url = "https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions"
    response = requests.request("GET", url, params={
        "begin_ts": begin_ts,
        "build": 0,
        "mobi_app": "web"
    }, headers=get_gene_headers())
    return return_checker(response, ret_models=models.ChatSessions)


def get_chat_history(talker_id, session_type=1, limit=50) -> models.ChatSessionHistory:
    """
    获取历史消息
    :param talker_id: 对方ID
    :param session_type: 1为用户, 2为粉丝团
    :param limit: 拉取条数
    """
    url = "https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs"
    params = {
        "sender_device_id": 1,
        "talker_id": talker_id,
        "session_type": session_type,
        "size": limit,
        "build": 0,
        "mobi_app": "web"
    }
    response = requests.request("GET", url, params=params, headers=get_gene_headers())
    return return_checker(response, ret_models=models.ChatSessionHistory)

def upload_image(filename: str) -> models.UploadImage:
    f = open(filename, 'rb')
    try:
        url = "https://api.bilibili.com/x/dynamic/feed/draw/upload_bfs"
        payload = {'biz': 'im',
                   'csrf': '8ec848ff9c1377eb074c137698c1b8e8',
                   'build': '0',
                   'mobi_app': 'web'}
        im_type = imghdr.what(f)
        if im_type is None:
            raise TypeError(f"invalid image: {filename}")
        files = [
            ('file_up', ('falconlove.png', f, f'image/{im_type}'))
        ]
        response = requests.request("POST", url, headers=get_gene_headers(), data=payload, files=files)
        return return_checker(response, ret_models=models.UploadImage)
    finally:
        f.close()

def send_chat_message(receiver_id, send_msg, msg_type=1, receiver_type=1, msg_status=0, sender_uid=None, csrf=None):
    """
    发送私信
    :param receiver_id: 接收者uid
    :param send_msg: msg_type 为 1: 纯文本; msg_type 为 5: 消息id; msg_type 为 2: 图片url
    :param msg_type: 1:发送文字 2:发送图片 5:撤回消息
    :param receiver_type: 1
    :param msg_status: 0
    :param sender_uid: 发送者mid
    :param csrf: csrf
    :return: msg_key -> int
    """
    url = "https://api.vc.bilibili.com/web_im/v1/web_im/send_msg"
    payload = {
        "msg[sender_uid]": sender_uid if sender_uid is not None else get_self_uid(),
        "msg[receiver_id]": receiver_id,
        "msg[receiver_type]": receiver_type,
        "msg[msg_type]": msg_type,
        "msg[msg_status]": msg_status,
        "msg[dev_id]": BiliCfg.device_id,
        "msg[timestamp]": int(time.time()),
        "csrf": get_csrf() if csrf is None else csrf
    }
    if msg_type == 1:
        payload["msg[content]"] = json.dumps({"content": send_msg}, ensure_ascii=False)
    elif msg_type == 5:
        payload["msg[content]"] = send_msg
    elif msg_type == 2:
        if isinstance(send_msg, models.UploadImage):
            _data = {
                "url": send_msg.data.image_url,
                "height": send_msg.data.image_height,
                "width": send_msg.data.image_width,
                # "imageType": "jpeg",
                # "original": 1,
                # "size": 147
            }
        else:
            _data = {
                "url": send_msg
            }
        payload["msg[content]"] = json.dumps(_data, ensure_ascii=False)

    response = requests.request("POST", url, headers=get_gene_headers(), data=payload)
    resp_data = json.loads(return_checker(response))
    return resp_data["data"]["msg_key"]


def fast_reply_chat(ctx: models.ChatSessionHistoryMessage, content: t.Optional[str] = None,
                    image_path: t.Optional[str] = None) -> t.Optional[t.Union[int, str]]:
    """
    回复消息
    :param ctx: ChatSessionHistoryMessage
    :param content: 消息文本
    :param image_path: 图片路径
    :return: 消息ID (msg_key)
    """
    if content is not None:
        return send_chat_message(ctx.sender_uid, content, msg_type=1)
    if image_path is not None:
        upd_im = upload_image(image_path)
        return send_chat_message(287061163, upd_im, msg_type=2)

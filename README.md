# bilibili-bot
- 简单的b站 评论区/私聊bot sdk, 可以根据关键词回复 评论区艾特bot的消息和私聊消息
- 插件化开发
- **未测试应援团消息**



# 开发

### 插件开发

------


- 打开`plugins`文件夹, 新建一个包
  - 怎么新建包: 创建一个文件夹, 在里面添加`__init__.py`

- 插件代码例 ([/plugins/hello/reg.py](/blob/main/plugins/hello/reg.py)):

```python
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

```



### 账号配置

----

- 打开`bili_config.json`
- 在`cookies`字段出粘贴您的完整cookie
- `cookieIndex`字段表示您需要使用`cookies`中的哪个cookie

```json
{
    "bili": {
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62",
        "cookies": [
            "从浏览器复制您的完整cookie, 然后粘贴至此处"
        ],
        "cookieIndex": 0,
        "device_id": null
    }
}
```



### 启动Bot

----

- 安装`Python 3.8`及以上版本
- 安装`requirements.txt`中的依赖

```shell
python -m pip install -r requirements.txt
```

- 执行`main.py`即可 `python main.py`

```python
import bot_core

bot = bot_core.BiliBot()
bot.run(10, 10)  # 第一个参数表示刷新秒数间隔, 数值越小, bot回复消息速度越快(越容易寄), 第二个参数为刷新秒数随机偏移值
```



### 效果测试

----

- 若您使用了上文给出的插件例程, 此时, 您的bot应该能做到:
  - 在任意评论区(或发动态)发送`@你的bot nihao`, bot将在相应评论/动态下回复`Hello World!`
  - 私聊发送`nihao`, bot回复 `Hello World!`
  - 私聊发送`/testimg`, bot向您发送一张图片
  - 私聊发送`/echo xxx`, bot将会复读您发送的`xxx`



# 补充信息

### 注册函数解释

----

- `CommandRegister.reg_startswith`: 匹配所有以`参数1`**开头**的消息
- `CommandRegister.reg_endswith`: 匹配所有以`参数1`**结尾**的消息
- `CommandRegister.reg_starts_and_endswith`: 匹配所有以`参数1`开头**和**`参数2`结尾的消息
- `CommandRegister.reg_exactly_match`: 匹配所有与`参数1`**完全相同**的消息
- `CommandRegister.reg_regex`: 匹配所有匹配`参数1`给出的**正则**的消息

#### 注册函数中`allowed_type`参数的用处

- 需要传入一个列表, 列表内容为`BotCodes`成员

| 匹配消息类型             | `ctx`类型                 | 备注              |
| ------------------------ | ------------------------- | ----------------- |
| BotCodes.AT_MESSAGE      | AtMessageItem             | 评论区艾特Bot消息 |
| BotCodes.PRIVATE_MESSAGE | ChatSessionHistoryMessage | 私聊消息          |
| BotCodes.GROUP_MESSAGE   | ChatSessionHistoryMessage | 应援团消息        |



# TODO

 - 目前sdk内没有集成收发消息以外的API, 若需要获取B站用户信息等, 可以参考 [/bili_api/api.py](/blob/main/bili_api/api.py) 的写法和 [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 这个仓库内的API自行添加, 欢迎pr~


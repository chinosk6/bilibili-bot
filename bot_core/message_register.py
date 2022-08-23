import re
from .bot_codes import BotCodes, regist_func_count

st_msg = [  # 匹配开头
    # ["/hello", plugins.hello.say_hello, [BotCodes.Message.TYPE_GUILD_MESSAGE]]
]

ed_msg = [  # 匹配结尾
]

sd_msg = [  # 匹配开头 && 结尾
    # ["st", "ed", None, [BotCodes.Message.TYPE_GUILD_MESSAGE]]
]

r_msg = [  # 正则匹配
]

ex_msg = [  # 完全匹配
]

default_allowed_type = [BotCodes.AT_MESSAGE]

def add_reg_func_count(allowed_type: list):
    for i in allowed_type:
        if i not in regist_func_count:
            regist_func_count[i] = 0
        regist_func_count[i] += 1

class CommandRegister:
    @staticmethod
    def reg_startswith(command: str, allowed_type=None):
        if allowed_type is None:
            allowed_type = default_allowed_type
        global st_msg
        add_reg_func_count(allowed_type)

        def c_func(func):
            st_msg.append([command, func, allowed_type])
            return func
        return c_func

    @staticmethod
    def reg_endswith(command: str, allowed_type=None):
        if allowed_type is None:
            allowed_type = default_allowed_type
        global ed_msg
        add_reg_func_count(allowed_type)

        def c_func(func):
            ed_msg.append([command, func, allowed_type])
            return func
        return c_func

    @staticmethod
    def reg_starts_and_endswith(command_st: str, command_ed: str, allowed_type=None):
        if allowed_type is None:
            allowed_type = default_allowed_type
        global sd_msg
        add_reg_func_count(allowed_type)

        def c_func(func):
            sd_msg.append([command_st, command_ed, func, allowed_type])
            return func
        return c_func

    @staticmethod
    def reg_regix(regix: str, allowed_type=None):
        if allowed_type is None:
            allowed_type = default_allowed_type
        global r_msg
        add_reg_func_count(allowed_type)

        def c_func(func):
            r_msg.append([regix, func, allowed_type])
            return func
        return c_func

    @staticmethod
    def reg_exactly_match(command: str, allowed_type=None):
        if allowed_type is None:
            allowed_type = default_allowed_type
        global ex_msg
        add_reg_func_count(allowed_type)

        def c_func(func):
            ex_msg.append([command, func, allowed_type])
            return func
        return c_func


class Matcher:

    @staticmethod
    def startswith(msg_content: str, msg_type):
        ret = []
        for cmds in st_msg:
            cmd, func, allowed = cmds
            if msg_type in allowed:
                if msg_content.startswith(cmd):
                    ret.append([func, msg_content[len(cmd):]])
        return ret

    @staticmethod
    def endswith(msg_content: str, msg_type):
        ret = []
        for cmds in ed_msg:
            cmd, func, allowed = cmds
            if msg_type in allowed:
                if msg_content.startswith(cmd):
                    ret.append([func, msg_content[:-len(cmd)]])
        return ret

    @staticmethod
    def starts_and_endswith(msg_content: str, msg_type):
        ret = []
        for cmds in sd_msg:
            cmd_start, cmd_end, func, allowed = cmds
            if msg_type in allowed:
                if msg_content.startswith(cmd_start) and msg_content.endswith(cmd_end):
                    ret.append([func, msg_content[len(cmd_start):-len(cmd_end)]])
        return ret

    @staticmethod
    def msg_regix(msg_content: str, msg_type):
        ret = []
        for cmds in r_msg:
            cmd, func, allowed = cmds
            if msg_type in allowed:
                if re.findall(cmd, msg_content):
                    ret.append([func, msg_content])
        return ret

    @staticmethod
    def msg_ex(msg_content: str, msg_type):
        ret = []
        for cmds in ex_msg:
            cmd, func, allowed = cmds
            if msg_type in allowed:
                if msg_content == cmd:
                    ret.append([func, msg_content])
        return ret


def get_matching_methods(msg_content: str, msg_type):
    st = Matcher.startswith(msg_content, msg_type)
    ed = Matcher.endswith(msg_content, msg_type)
    st_ed = Matcher.starts_and_endswith(msg_content, msg_type)
    rx = Matcher.msg_regix(msg_content, msg_type)
    ex = Matcher.msg_ex(msg_content, msg_type)
    return st + ed + st_ed + rx + ex

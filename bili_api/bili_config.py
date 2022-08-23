import json
from typing import List, Optional
import random


with open("bili_config.json", "r", encoding="utf8") as f:
    config_data: dict = json.load(f)
    _read_dev_id = config_data["bili"]["device_id"]


def generate_device_id():
    b = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    s = list("xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx")
    for n, i in enumerate(s):
        if i in ["-", "4"]:
            continue
        randInt = random.randint(0, 15)
        if i == "x":
            s[n] = b[randInt]
        else:
            s[n] = b[3 & randInt | 8]
    return "".join(s)


class BiliCfg:
    ua: str = config_data["bili"]["ua"]
    cookies: List[str] = config_data["bili"]["cookies"]
    cookieIndex: Optional[int] = config_data["bili"]["cookieIndex"]
    device_id: str = generate_device_id() if _read_dev_id is None else _read_dev_id

    @staticmethod
    def refresh_device_id():
        BiliCfg.device_id = generate_device_id()

import requests
import userService
import error
import json
import time

SUCCESS = True
FAIL = False

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
}


def isSuccessRespond(raw_respond):
    respond_dict = json.loads(raw_respond.content.decode("utf-8"))
    try:

        respond_state = respond_dict["m"]
        if respond_state == "操作成功":
            return SUCCESS
        else:
            return FAIL
    except:
        error.reportError(error.netRespondError)
        return FAIL




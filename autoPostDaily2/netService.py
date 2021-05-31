import requests
from autoPostDaily2 import userService
from autoPostDaily2 import error
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


def userGetSessionCookies(user):
    try:
        user.net_session = requests.session()
        url1 = "https://app.buaa.edu.cn/site/buaaStudentNcov/index"
        user.net_session.get(url1, headers=headers)
        url3 = "https://app.buaa.edu.cn/wap/setting/info"
        user.net_session.get(url3, headers=headers)
        url2 = "https://app.buaa.edu.cn/buaaxsncov/wap/default/get-info"
        user.net_session.get(url2, headers=headers)

    except:
        error.reportError(error.netGetError)


def userLogIn(user):
    if user.information._certification_name== "" or user.information._certification_password== "":
        error.reportError(error.noLoginUrlError)
        return 0
    else:
        log_information = dict()
        log_information["username"] = user.information._certification_name
        log_information["password"] = user.information._certification_password
        url = "https://app.buaa.edu.cn/uc/wap/login/check"
        respond = user.net_session.post(url, headers=headers, data=log_information)
        if isSuccessRespond(respond) == FAIL:
            error.reportError(error.netRespondError)
        pass


def userGetConfig(user):
    try:
        url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/get-info"
        respond = user.net_session.get(url, headers=headers)
        if isSuccessRespond(respond) == FAIL:
            error.reportError(error.netRespondError)
            return
        else:
            all_status = json.loads(respond.content.decode("utf-8"))
            session_info = all_status["d"]["info"]
            user_info = all_status["d"]["uinfo"]

            user.information.realName = str(user_info["realname"])
            user.information.uid = str(user_info["uid"])
            user.information.number = str(user_info["role"]["number"])
            user.information.date = str(session_info["date"])
            user.information.id = str(session_info["id"])

    except:
        error.reportError(error.netRespondError)
        return


def userGenerateTimeStamp(user):
    user.information.created = str(int(time.time()))


def userPostForm(user, userPackage):
    try:
        session = user.net_session
        url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/save"
        respond = session.post(url, data=userPackage, headers=headers)
        # print(respond)
        if isSuccessRespond(respond) is FAIL:
            error.reportError(error.netRespondError)
    except:
        error.reportError(error.netPostError)






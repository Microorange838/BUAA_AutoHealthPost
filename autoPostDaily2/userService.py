import json
import requests
import error
from netService import *


# These three classes must add private attributes    !!!!
class Information(object):

    realName = ""
    number = "0"
    uid = "0"
    created = ""
    date = ""
    id = ""
    gwszdd = ""


class Position(object):
    area = "北京市 海淀区"
    city = "北京市"
    province = "北京市"
    address = "北京市海淀区花园路街道学生10宿舍北京航空航天大学学院路校区"
    geo_api_info = '{"type":"complete","info":"SUCCESS","status":1,"$Da":"jsonp_361934_","position":{"Q":39.98311,' \
                   '"R":116.34672,"lng":116.34672,"lat":39.98311},"message":"Get ipLocation success.Get address ' \
                   'success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{' \
                   '"citycode":"010","adcode":"110108","businessAreas":[{"name":"五道口","id":"110108","location":{' \
                   '"Q":39.99118,"R":116.34157800000003,"lng":116.341578,"lat":39.99118}}],' \
                   '"neighborhoodType":"生活服务;生活服务场所;生活服务场所","neighborhood":"北京航空航天大学","building":"学生10宿舍",' \
                   '"buildingType":"商务住宅;住宅区;宿舍","street":"北四环中路辅路","streetNumber":"244号","country":"中国",' \
                   '"province":"北京市","city":"","district":"海淀区","township":"花园路街道"},' \
                   '"formattedAddress":"北京市海淀区花园路街道学生10宿舍北京航空航天大学学院路校区","roads":[],"crosses":[],"pois":[]} '

    def generateGPSInfo(self, latitude, longtitude):
        info_dict = Position.generateGPSInfoDict()
        position_dict = info_dict["position"]

        position_dict["Q"] = "{:.5f}".format(latitude)
        position_dict["lat"] = "{:.5f}".format(latitude)
        position_dict["R"] = "{:.5f}".format(longtitude)
        position_dict["lng"] = "{:.5f}".format(longtitude)
        self.geo_api_info = json.dumps(info_dict)

    def generateGPSInfoDict(self):
        info_dict = json.loads('{"type":"complete","info":"SUCCESS","status":1,"$Da":"jsonp_361934_","position":{"Q":39.98311,' 
                   '"R":116.34672,"lng":116.34672,"lat":39.98311},"message":"Get ipLocation success.Get address ' 
                   'success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{' 
                   '"citycode":"010","adcode":"110108","businessAreas":[{"name":"五道口","id":"110108","location":{' 
                   '"Q":39.99118,"R":116.34157800000003,"lng":116.341578,"lat":39.99118}}],' 
                   '"neighborhoodType":"生活服务;生活服务场所;生活服务场所","neighborhood":"北京航空航天大学","building":"学生10宿舍",' 
                   '"buildingType":"商务住宅;住宅区;宿舍","street":"北四环中路辅路","streetNumber":"244号","country":"中国",' 
                   '"province":"北京市","city":"","district":"海淀区","township":"花园路街道"},' 
                   '"formattedAddress":"北京市海淀区花园路街道学生10宿舍北京航空航天大学学院路校区","roads":[],"crosses":[],"pois":[]} ')

        return info_dict


class Selection(object):
    sfzs = "1"
    bzxyy = ""
    bzxyy_other = ""
    brsfzc = "1"
    tw = ""
    sfcxzz = ""
    zdjg = ""
    zdjg_other = ""
    sfgl = ""
    gldd = ""
    gldd_other = ""
    glyy = ""
    glyy_other = ""
    gl_start = ""
    gl_end = ""
    sfmqjc = ""
    sfzc_14 = "1"
    sfqw_14 = "0"
    sfqw_14_remark = ""
    sfzgfx = "0"
    sfzgfx_remark = ""
    sfjc_14 = "0"
    sfjc_14_remark = ""
    sfjcqz_14 = "0"
    sfjcqz_14_remark = ""
    sfgtjz_14 = "0"
    sfgtjz_14_remark = ""
    szsqqz = "0"
    sfyqk = ""
    szdd = "1"

    gwdz = ""
    is_move = "0"
    move_reason = ""
    move_remark = ""


# This class is used for handle user
class User(object):
    def __init__(self, student_number, password):
        self.information = Information()
        self.position = Position()
        self.selection = Selection()
        self.student_number = student_number
        self.password = password
        self.net_session = requests.session()

    def generateUserPackage(self):
        information = self.information
        position = self.position
        selection = self.selection
        if isinstance(information, Information) and isinstance(position, Position) and isinstance(selection, Selection):
            return self.__generateUserDictUnprotected(information, position, selection)
        else:
            error.reportError(error.userDataError)

    def __generateUserDictUnprotected(self, information, position, selection):
        result = dict()

        for eachAttr in information.__dir__():
            if eachAttr[0] != '_' and isinstance(information.__getattribute__(eachAttr), str):
                result[eachAttr] = information.__getattribute__(eachAttr)
        for eachAttr in position.__dir__():
            if eachAttr[0] != '_' and isinstance(position.__getattribute__(eachAttr), str):
                result[eachAttr] = position.__getattribute__(eachAttr)
        for eachAttr in selection.__dir__():
            if eachAttr[0] != '_' and isinstance(selection.__getattribute__(eachAttr), str):
                result[eachAttr] = selection.__getattribute__(eachAttr)

        return result

    def oneKeyPost(self):
        self.init()
        if self.isPosted() is False:
            print("Try to post for {}".format(self.student_number))
            self.generateTimeStamp()
            user_package = self.generateUserPackage()
            self.postPackage(user_package)

    def init(self):
        self.__getSessionCookies()
        self.__logIn()
        self.__getConfig()

    def __getSessionCookies(self):
        try:
            url1 = "https://app.buaa.edu.cn/site/buaaStudentNcov/index"
            self.net_session.get(url1, headers=headers)
            url3 = "https://app.buaa.edu.cn/wap/setting/info"
            self.net_session.get(url3, headers=headers)
            url2 = "https://app.buaa.edu.cn/buaaxsncov/wap/default/get-info"
            self.net_session.get(url2, headers=headers)

        except:
            error.reportError(error.netGetError)

    def __logIn(self):
        if self.student_number == "" or self.password == "":
            error.reportError(error.noLoginUrlError)
            return 0
        else:
            log_information = dict()
            log_information["username"] = self.student_number
            log_information["password"] = self.password
            url = "https://app.buaa.edu.cn/uc/wap/login/check"
            respond = self.net_session.post(url, headers=headers, data=log_information)
            if isSuccessRespond(respond) == FAIL:
                error.reportError(error.netRespondError)
            pass

    def __getConfig(self):
        try:
            url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/get-info"
            respond = self.net_session.get(url, headers=headers)
            if isSuccessRespond(respond) == FAIL:
                error.reportError(error.netRespondError)
                return
            else:
                all_status = json.loads(respond.content.decode("utf-8"))
                session_info = all_status["d"]["info"]
                user_info = all_status["d"]["uinfo"]

                self.information.realName = str(user_info["realname"])
                self.information.uid = str(user_info["uid"])
                self.information.number = str(user_info["role"]["number"])
                self.information.date = str(session_info["date"])
                self.information.id = str(session_info["id"])

        except:
            error.reportError(error.netRespondError)
            return

    def generateTimeStamp(self):
        self.information.created = str(int(time.time()))

    def postPackage(self, userPackage):
        try:
            session = self.net_session
            url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/save"
            respond = session.post(url, data=userPackage, headers=headers)
            # print(respond)
            if isSuccessRespond(respond) is FAIL:
                error.reportError(error.netRespondError)
        except:
            error.reportError(error.netPostError)

    def isPosted(self):
        try:
            url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/get-info"
            respond = self.net_session.get(url, headers=headers)
            if isSuccessRespond(respond) == FAIL:
                error.reportError(error.netRespondError)
                return
            else:
                all_status = json.loads(respond.content.decode("utf-8"))
                return all_status['d']['hasFlag']
        except:
            error.reportError(error.netRespondError)
            return





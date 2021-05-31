from userService import *
from netService import *


if __name__ == "__main__":
    gwz = userService.User()
    userGetSessionCookies(gwz)
    gwz.information._certification_name = "你的学号"
    gwz.information._certification_password = "你的密码"
    userLogIn(gwz)
    userGetConfig(gwz)
    userGenerateTimeStamp(gwz)
    user_package = gwz.generateUserPackage()
    userPostForm(gwz, user_package)

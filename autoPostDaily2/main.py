from userService import *
from netService import *
import time

postConfig = {
    "time_hour" : 17,
    "time_minute" : 30,
    "user_list" : []
}


def readConfig(filename="config"):
    file = open(filename, 'r', encoding="utf-8")
    text = file.read()
    lines = text.split('\n')
    postConfig["time_hour"] = int(lines[0].split(' ')[0])
    postConfig["time_minute"] = int(lines[0].split(' ')[1])
    lines.pop(0)
    for each_line in lines:
        now_user = User(each_line.split(' ')[0], each_line.split(' ')[1])
        postConfig["user_list"].append(now_user)


def waitToPost():
    while 1:

        now_time = time.localtime()
        now_min = now_time.tm_min
        now_hour = now_time.tm_hour

        if now_min==postConfig["time_minute"] and now_hour==postConfig["time_hour"]:
            print("----------Time Stamp {} {} {}---------".format(str(now_time.tm_year), str(now_time.tm_hour), str(now_time.tm_min)))
            for each_user in postConfig["user_list"]:

                each_user.oneKeyPost()

        time.sleep(30)


def main():
    readConfig()
    waitToPost()


if __name__ == "__main__":
    main()

class GError(Exception):
    errorLevel = 0
    context = ""


userDataError = GError()
userDataError.errorLevel = 1
userDataError.context = "fail to convert->invalid user data"

netPostError = GError()
netPostError.errorLevel = 2
netPostError.context = "fail to post form"

netRespondError = GError()
netRespondError.errorLevel = 2
netRespondError.context = "remote server respond wrong"

netGetError = GError()
netGetError.errorLevel = 2
netGetError.context = "fail to get data from website"

noLoginUrlError = GError()
noLoginUrlError.errorLevel = 2
noLoginUrlError.context = "invalid name or password or loginurl"

def reportError(gerror):
    print("[{}]{}".format(str(gerror.errorLevel), gerror.context))


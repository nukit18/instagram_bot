import os


def get_path():
    global wpath
    wpath = os.getcwd()


async def get_logins():
    path = wpath + "/logins.txt"
    file = open(path, 'r')
    arr_logins = file.read().split()
    logins = {}
    for i in range(0, len(arr_logins), 2):
        logins[f"{arr_logins[i]}"] = f"{arr_logins[i+1]}"
    return logins


if __name__ == '__main__':
    get_path()
    print(wpath)
    for login in get_logins():
        print(login)
    print(get_logins())

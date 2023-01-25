import requests

import math
# Working with yandex.disk API
CLIENT_ID = 'c58fb0815b604b5e993a77436abd601c'
CLIENT_SECRET = '77d4a30a07794dbca9a48c0064e0b432'
REDIRECT_URL = 'https://oauth.yandex.ru/verification_code'

BASE_AUTH_URL = 'https://oauth.yandex.ru/authorize'


def get_token():
    print("Enter to the link and give access")
    print(f"{BASE_AUTH_URL}?response_type=code&client_id={CLIENT_ID}")
    code = input("Enter the code: ")
    response = requests.post("https://oauth.yandex.ru/token", data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    if response.status_code != 200:
        print(response.json())
        return
    return response.json()["access_token"]


def get_info(token: str):
    response = requests.get('https://cloud-api.yandex.net/v1/disk/', headers={'Authorization': f'OAuth {token}'})
    return response.json()


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def run():
    token = get_token()
    if not token:
        print("I DIDN'T GET TOKEN :(")
        return
    info = get_info(token)
    print("Total space: ", convert_size(info['total_space']),
          "\nUsed space: ", convert_size(info["used_space"]),
          "\nTrash size: ", convert_size(info['trash_size']))


if __name__ == '__main__':
    run()

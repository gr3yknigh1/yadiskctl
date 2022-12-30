#!/usr/bin/env python
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any
import os
import os.path
import webbrowser

import yandex

__version__ = "0.1"

HOME_PATH = os.path.expanduser("~")
STATE_PATH = os.path.join(HOME_PATH, ".local", "state", "yadisk")
KEY_PATH = os.path.join(STATE_PATH, "oauth_code")
TOKEN_PATH = os.path.join(STATE_PATH, "token")
if not os.path.exists(STATE_PATH):
    os.makedirs(STATE_PATH)


# TODO: Handle wrong syntax
def get_dotenv(dotenv_path: str = ".env") -> dict[str, Any]:
    env = {}
    with open(dotenv_path, mode="r") as f:
        for line in filter(lambda x: x != "", f.read().split("\n")):
            name, value = line.split("=")
            env[name] = value
    return env

def load_dotenv_to_environ(dotenv_path: str = ".env") -> None:
    os.environ.update(get_dotenv(dotenv_path))


def get_oauth_code() -> str:
    oauth_code: str = ""

    if not os.path.exists(KEY_PATH):
        CLIENT_ID = os.environ["CLIENT_ID"]
        REDIRECT_URL = os.environ["REDIRECT_URL"]
        OAUTH_CODE_REQUREST = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}"

        wb = webbrowser.get()
        wb.open_new_tab(OAUTH_CODE_REQUREST)

        oauth_code = input("Paste oauth code: ")

        with open(KEY_PATH, mode="x") as f:
            f.write(oauth_code)
    else:
        with open(KEY_PATH, mode="r") as f:
            oauth_code = f.read().split("\n")[0]
    return oauth_code


def get_token() -> str:
    token: str = ""

    if not os.path.exists(TOKEN_PATH):
        CLIENT_ID = os.environ["CLIENT_ID"]
        TOKEN_REQUREST = f"https://oauth.yandex.ru/authorize?response_type=token&client_id={CLIENT_ID}"

        wb = webbrowser.get()
        wb.open_new_tab(TOKEN_REQUREST)

        token = input("Paste token: ")

        with open(TOKEN_PATH, mode="x") as f:
            f.write(token)
    else:
        with open(TOKEN_PATH, mode="r") as f:
            token = f.read().split("\n")[0]
    return token


def main() -> int:
    load_dotenv_to_environ()
    token = get_token()

    disk = yandex.YandexDisk(token)
    info = disk.get_disk_info()
    print(info)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

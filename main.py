#!/usr/bin/env python3
"""
Send email.mime.multipart.MIMEMultipart messages.
"""

from typing import List, Union
from webbrowser import get
from dotenv import load_dotenv
from os import environ
from uuid import uuid4
from textwrap import dedent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL, LMTP
from secrets import randbelow
from time import sleep
from pathlib import Path
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)


def get_addr_list(source_file: Path) -> List[str]:
    with source_file.open("r") as fp:
        return fp.readlines()


config = {
    "host": environ.get("MAIL_HOST", ""),
    "port": int(environ.get("MAIL_PORT", 2525)),
    "username": environ.get("MAILBOX_USERNAME", ""),
    "password": environ.get("MAILBOX_PASSWORD", ""),
} # Generated test mailbox on mailtrap.io

from_list: List[str] = get_addr_list(environ.get("FROM_LIST_FILE", Path("random_addrs.txt")))
to_list: List[str] = ["test-eiq-zed@wildduck.email"]


def create_msg_body(to_addr: str, nonce: str) -> str:
    # username = to_addr
    # if "@" in to_addr:
    #     username = to_addr.split("@")[0]

    out = f'''
    Hello {to_addr}!

    This is an arbitrary message.
    Happy hunting!

    Msg nonce: {nonce}
    '''

    return dedent(out)


def create_msg(from_addr: str, to_addr: str, subject: str, nonce: str) -> str:
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = f"{subject} - {nonce}"

    msg.attach(MIMEText(create_msg_body(to_addr, nonce), "plain"))

    return msg


def send_msg(mail_client: SMTP, from_addr: str, to_addr: str, subject: str, nonce: str):
    mail_client.send_message(create_msg(from_addr, to_addr, subject, nonce), from_addr, to_addr)


def send_msgs_generate_random(server: Union[SMTP,LMTP], from_list: str, to_list: str, subject: str, nonce: str, num_to_send: int):
    for i in range(1,num_to_send):
        _from = from_list[randbelow(len(from_list))-1]
        _to = to_list[randbelow(len(to_list))-1]
        send_msg(server, _from, _to, "RE: this issue", uuid4())
        sleep(2)

def main():
    NUM_MSGS = 40
    if config["host"] in ("localhost", "127.0.0.1"):
        with LMTP(config["host"], config["port"]) as server:
            #server.login(config["username"], config["password"])
            send_msgs_generate_random(server, from_list, to_list, "RE: this issue", uuid4(), NUM_MSGS)
    else:
        logging.info(f"Connecting to {config['host']}:{config['port']}...")
        with SMTP_SSL(config["host"], config["port"]) as server:
            server.login(config["username"], config["password"])
            logging.info("🎉 Success")
            send_msgs_generate_random(server, from_list, to_list, "RE: this issue", uuid4(), NUM_MSGS)




if __name__ == "__main__":
    main()

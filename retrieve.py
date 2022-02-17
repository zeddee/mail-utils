import imaplib
from multiprocessing.spawn import prepare
from os import environ
from typing import List, Union
from time import sleep

def prepare_criteria(to_keyword: Union[str, bool], from_keyword: Union[str, bool], subject_keyword: Union[str, bool]) -> List[str]:
    out = []
    if to_keyword:
        out.append('(TO "{}")'.format(to_keyword))
    if from_keyword:
        out.append('(FROM "{}")'.format(from_keyword))
    if subject_keyword:
        out.append('(SUBJECT "{}")'.format(subject_keyword))
    else:
        out = ["ALL"]

    return out


def get_messages(server: imaplib.IMAP4, res: List[bytes]):
    msgs = []
    for msg_id in res[0].split(b" "):
        status, res = server.fetch(msg_id, "(RFC822)")
        if status != "OK":
          raise Exception(status, res)
        msgs.append(res)
        
    print(msgs)
    print(f"Count: {len(msgs)}")


# with imaplib.IMAP4("smtp.mailtrap.io", 2525) as server:
with imaplib.IMAP4_SSL("localhost", 9993) as server:
    server.login("zed@shootbird.work", "pass")

    criteria = prepare_criteria(
      environ.get("TO_KEYWORD", False),
      environ.get("FROM_KEYWORD", False),
      environ.get("SUBJECT_KEYWORD", False),
    )
    status, res = server.select("INBOX")
    if status != "OK":
      raise Exception(status, res)
    

    status, res = server.search("UTF-8", *criteria)

    if status != "OK":
      raise Exception(status, res)

    get_messages(server, res)
from uuid import uuid4
from pathlib import Path
from typing import List
from os import environ


OUTPUT_FILE=environ.get("OUTPUT_FILE", "./random_addrs.txt")


def generate_random_addrs(max_num: int) -> List[str]:
    out = []
    for i in range(1, max_num):
        out.append(f"{uuid4()}@{'mail.test57fe2f.nsdmdh.com'}")

    return out


def write_file(destination: Path):
    with destination.open("w") as fp:
        fp.write("\n".join(generate_random_addrs(10)))


if __name__ == "__main__":
    write_file(Path(OUTPUT_FILE))
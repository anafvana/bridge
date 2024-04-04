import argparse
import re
import time
from pathlib import Path
from typing import TextIO


def copy_file(src_path: Path, dest_path: Path, bridge_io: TextIO):
    # Write contents to bridge
    bridge_io.write(r'contents = """')
    with open(src_path, "r") as src_io:
        for line in src_io:
            bridge_io.write(line)
    bridge_io.write(r'"""')

    # Literal block: Write to destination file
    bridge_io.write(rf"""
dest_path = Path('./{dest_path}')
dest_path.unlink(missing_ok=True)
with open(dest_path, "w+") as dest_io:
    dest_io.write(contents)
""")


def make_dir(dest_path: Path, bridge_io: TextIO):
    bridge_io.write(rf"""
dest_path = Path('./{dest_path}')
dest_path.mkdir(exist_ok=True, parents=True)
""")


def contains_patterns(path: str | Path, excluded_patterns: list[str]) -> bool:
    path = path.__str__() if isinstance(path, Path) else path

    for r in excluded_patterns:
        if re.match(pattern=r, string=path):
            return True

    return False


def create_bridge(origin: Path, excluded_patterns: list[str]):
    target = Path("./output")
    bridge_file = Path("bridge.py")
    src_paths = filter(lambda x: not contains_patterns(x, excluded_patterns), origin.rglob("*"))

    bridge_file.unlink(missing_ok=True)

    with open(bridge_file, 'w+') as bridge_io:
        bridge_io.write("""#!/usr/bin/env python3
        
from pathlib import Path
""")
        for src_path in src_paths:
            dest_path = target / src_path.relative_to(origin)

            if src_path.is_dir():
                make_dir(dest_path=dest_path, bridge_io=bridge_io)
            elif src_path.is_file():
                copy_file(src_path=src_path, dest_path=dest_path, bridge_io=bridge_io)
            else:
                print(f"WARNING: {src_path} is neither file nor directory")

    bridge_file.chmod(777)


def error_and_quit(msg:str):
    print(msg)
    time.sleep(.3)
    print("TERMINATING")
    time.sleep(.3)
    exit(1)

if __name__ == "__main__":
    # ------ PATH ------ #
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path of folder to copy", type=str, required=True)
    args = parser.parse_args()

    origin_path = Path(args.path)
    if not origin_path.exists():
        error_and_quit(f"Path '{origin_path}' does not exist.")

    if not origin_path.is_dir():
        error_and_quit(f"Path '{origin_path}' is not a directory.")

    # ------ EXCLUSIONS ------ #
    exclusions: list[str] = [
        r'.*\.git.*',
        r'.*\.md',
        r'.*/key-files/?.*'
    ]

    # ------ RUN ------ #
    create_bridge(origin_path, exclusions)


#     ____ origin                         bridge_file               ____ target
#    /    \__________________          =================           /    \__________________
#    |                       |         =================           |                       |
#    |  ___ src              |         =================           |  ___ dest             |
#    | /   \________         |         =================           | /   \________         |
#    | |            |        |   ⇒     =================     ⇒     | |            |        |
#    | |  ■src_file |        |         =================           | |  ■dest_file|        |
#    | +------------         |         =================           | +------------         |
#    +-----------------------+         =================           +-----------------------+

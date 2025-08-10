import os

import pipepy
from pipepy import uv

pipepy.set_always_stream(True)
pipepy.set_always_raise(True)


def test():
    "Run tests"

    uv.run.pytest()


def examples():
    "Run all examples"

    for filename in os.listdir("src/examples"):
        if filename.endswith(".py") and not filename.startswith("_"):
            print(f"# {filename}\n")
            uv.run(f"src/examples/{filename}")()
            print()

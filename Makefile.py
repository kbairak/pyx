import os
import random

import pipepy
from pipepy import uv

pipepy.set_always_stream(True)
pipepy.set_always_raise(True)


def test():
    "Run tests"

    uv.run.pytest()


def examples():
    "Run all examples"

    filenames = os.listdir("src/examples")
    random.shuffle(filenames)
    for filename in filenames:
        if filename.endswith(".py") and not filename.startswith("_"):
            print(f"# {filename}\n")
            uv.run(f"src/examples/{filename}")()
            print()


def lint():
    "Run linters"

    uv.run.ruff.check(fix=True)()
    uv.run.ruff.format()

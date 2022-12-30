from __future__ import annotations
import os.path
import setuptools
import yadisk


def get_file_lines(file_path: str) -> list[str]:
    if not os.path.exists(file_path):
        raise FileExistsError(f"Can't find file with path: '{file_path}'")
    with open(file_path) as fs:
        lines = fs.read().split('\n')
    return lines


setuptools.setup(
    name="yadisk",
    version=yadisk.__version__,

    author="Akkuzin Ilya",
    author_email="gr3yknigh1@gmail.com",
    url="https://github.com/gr3yknigh1/yadisk",

    py_modules=["yadisk"],

    entry_points={
        "console_scripts": ["yadisk = yadisk:main"]
    },

    install_requires=get_file_lines("./requirements.txt"),
    extras_requires={
        "dev": get_file_lines("./requirements-dev.txt")
    },
    python_requires=">=3.10"
)

import io
import os
import re

from setuptools import find_packages, setup

REQUIREMENTS_FILE = "requirements.txt"


def parse_requirements() -> list:
    with open(REQUIREMENTS_FILE) as f:
        reqs = f.read().splitlines()
    reqs = [r.strip() for r in reqs if r.strip()]  # remove empty lines
    reqs = [r for r in reqs if not r.startswith("#")]  # remove line comments
    # remove comments
    reqs = [r.split("#", 1)[0].strip() if "#" in r else r for r in reqs]
    return reqs


def read(filename: str) -> str:
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="memory_copilot",
    version="0.1.0",
    url="https://github.com/Smilexuhc/memory_copilot",

    author="Smile",
    author_email="smile.xuhc@gmail.com",

    description="Your external memory and personal assistant",
    long_description=read("README.md"),

    packages=find_packages(exclude=('memory_copilot/experimental')),
    include_package_data=True,

    install_requires=parse_requirements(),
    entry_points={
        'console_scripts': [
            'mem-copilot = memory_copilot.cli:cli',
        ]
    }
)

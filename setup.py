#!/usr/bin/env python


from distutils.core import setup


setup(
    name="harbinger",
    version="0.0.1",
    description="Abstract remote shell connection through several libraries, "
    "designed for performance",
    author="Xavier Hardy",
    url="https://github.com/xavierhardy/harbinger",
    packages=[],
    extras_require={
        "paramiko": ["paramiko==2.4.1"],
        "ssh2": ["ssh2-python==0.15.0.post9"],
    },
)

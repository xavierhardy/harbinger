#!/usr/bin/env python

from harbinger.protocols.telnet import TelnetConnection

from sys import version_info
from getpass import getpass

PY3 = version_info[0] > 2
if PY3:
    raw_input = input


if __name__ == "__main__":
    print("Configuring Telnet connection")
    hostname = raw_input("Hostname: ")
    port = int(raw_input("Port: "))
    username = raw_input("Username: ")
    password = getpass()
    prompt = "%s@[^$]+\$" % username

    connection_data = {
        "hostname": hostname,
        "port": port,
        "username": username,
        "password": password,
        "prompt": prompt,
        "socket_timeout": 60,
        "timeout": 60,
    }

    print("Creating Telnet connection object")
    connection = TelnetConnection(**connection_data)
    print("Connecting")
    try:
        connection.connect()
        print("Sending 'ls'")
        connection.send("ls")
        print("Receiving output")
        print(connection.receive())
    finally:
        print("Disconnecting")
        connection.disconnect()
    print("Done")

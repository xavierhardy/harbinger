#!/usr/bin/env python

from harbinger.protocols.paramiko import ParamikoSshConnection

from sys import version_info
from getpass import getpass

PY3 = version_info[0] > 2
if PY3:
    raw_input = input


if __name__ == "__main__":
    print("Configuring SSH connection")
    hostname = raw_input("Hostname: ")
    port = int(raw_input("Port: "))
    username = raw_input("Username: ")
    password = getpass("Password (leave empty for key authentication): ")
    if not password:
        private_key_file = raw_input("Private key file: ")
        public_key_file = raw_input("Public key file [%s.pub]: " % private_key_file) or "%s.pub" % private_key_file
    else:
        private_key_file = None
        public_key_file = None

    prompt = "%s@[^$]+\$" % username

    connection_data = {
        "hostname": hostname,
        "port": port,
        "username": username,
        "password": password or None,
        "private_key_file": private_key_file,
        "prompt": prompt,
        "public_key_file": public_key_file,
        "socket_timeout": 60,
        "timeout": 60,
    }

    print("Creating SSH connection object")
    connection = ParamikoSshConnection(**connection_data)
    print("Connecting")
    try:
        connection.connect()
        print("Sending 'ls'")
        from time import sleep
        sleep(1)
        connection.send("ls")
        print("Receiving output")
        sleep(1)
        print(connection.receive())
    finally:
        print("Disconnecting")
        connection.disconnect()
    print("Done")

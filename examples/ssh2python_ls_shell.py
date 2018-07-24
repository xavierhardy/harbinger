#!/usr/bin/env python

from harbinger.protocols.telnet import TelnetConnection as SshConnection


if __name__ == '__main__':
    prompt = "user@localhost:/\$"
    connection_data = {
        "hostname": "localhost",
        "port": 22,
        "username": "user",
        "password": "user",
        "public_key_file": "/home/user/.ssh/id_rsa.pub",
        "private_key_file": "/home/user/.ssh/id_rsa",
        "prompt": prompt,
        "socket_timeout": 100,
        "timeout": 140,
    }
    connection = SshConnection(**connection_data)
    connection.connect()
    connection.send("ls")
    print(connection.receive())
    connection.disconnect()
    print("done")

    connection = SshConnection(**connection_data)
    print(connection.connected)
    connection.connect()
    print(connection.connected)
    connection.send("ls")
    print(connection.receive())
    connection.disconnect()
    print("done")
    with SshConnection(**connection_data) as connection:
        connection.send("ls")
        print(connection.connected)
        print(connection.receive())
        print(connection.connected)

    print(connection.connected)
    print("done")


    connection = SshConnection(**connection_data)
    print(connection.connected)
    connection.connect()
    print(connection.connected)
    connection.send("ls")
    print(connection.receive())
    connection.disconnect()
    print("done")

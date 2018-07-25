import re
from logging import getLogger, DEBUG, StreamHandler
from socket import _GLOBAL_DEFAULT_TIMEOUT
from sys import stdout
from telnetlib import Telnet
from time import time

from harbinger.base.shell import ShellConnection
from harbinger.exceptions import (
    ReceiveTimeoutException,
    SocketTimeoutException,
    ReceiveException,
)

LOG = getLogger(__name__)
LOG.setLevel(DEBUG)
handler = StreamHandler(stdout)
handler.setLevel(DEBUG)
LOG.addHandler(handler)

LOGIN_REGEX = re.compile("login\s*:", re.I)
PASSWORD_REGEX = re.compile("password\s*:", re.I)


class TelnetConnection(ShellConnection):
    socket = None
    channel = None
    session = None

    def connect(self, wait_prompt=True):
        port = self.port or 23
        socket_timeout = self.socket_timeout or _GLOBAL_DEFAULT_TIMEOUT
        self.session = Telnet(self.hostname, port, socket_timeout)
        self.channel = self.session
        self.socket = self.session.sock
        self.receive(LOGIN_REGEX)
        self.send(self.username)
        if self.password is not None:
            self.receive(PASSWORD_REGEX)
            self.send(self.password)
        if wait_prompt:
            self.receive()

    @property
    def connected(self):
        return bool(self.socket and not self.socket._closed and self.session)

    def send(self, line, socket_timeout=None):
        socket_timeout = (
            socket_timeout
            if socket_timeout is not None
            else self.socket_timeout
        )
        self.socket.settimeout(socket_timeout)
        size = self.channel.write((line + "\n").encode())
        return size

    def receive(
        self, regex=None, socket_timeout=None, timeout=None, buffer_size=None
    ):
        regex = regex if regex is not None else self.prompt_regex
        socket_timeout = (
            socket_timeout
            if socket_timeout is not None
            else self.socket_timeout
        )
        timeout = timeout if timeout is not None else self.timeout
        buffer_size = (
            buffer_size if buffer_size is not None else self.buffer_size
        )

        assert regex is not None
        assert socket_timeout is None or isinstance(
            socket_timeout, (int, float)
        )
        assert timeout is None or isinstance(timeout, (int, float))
        assert isinstance(buffer_size, int) and buffer_size > 0

        self.socket.settimeout(socket_timeout)
        start = time()
        output = self.channel.read_some().decode()
        LOG.debug(output)
        size = len(output)
        duration = time() - start
        while (
            not regex.search(output)
            and (timeout is None or duration < timeout)
            and size > 0
        ):
            data = self.channel.read_some().decode()
            LOG.debug(data)
            size = len(data)
            output += data
            duration = time() - start

        if size < 0:
            raise ReceiveException(size, output, duration)

        if not size:
            raise SocketTimeoutException(
                output, socket_timeout, duration, regex.pattern
            )

        if timeout is not None and duration >= timeout:
            raise ReceiveTimeoutException(
                output, timeout, duration, regex.pattern
            )

        return self.sanitize(output)

    def disconnect(self):
        self.session.close()
        self.socket.close()

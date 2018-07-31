from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM
from time import time

from paramiko import Transport, RSAKey, DSSKey

from harbinger.base.ssh import BaseSshConnection, DSA_KEY_ALGORITHM
from harbinger.exceptions import LIBSSH2_ERROR_EAGAIN
from harbinger.exceptions import (
    ReceiveTimeoutException,
    SocketTimeoutException,
    ReceiveException,
)

LOG = getLogger(__name__)


class ParamikoSshConnection(BaseSshConnection):
    def connect(self, wait_prompt=True):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))
        self.session = Transport(self.socket)
        self.session.start_client()
        if self.password is not None:
            self.session.auth_password(self.username, self.password)
        elif self.key_algorithm != DSA_KEY_ALGORITHM:
            key = RSAKey.from_private_key_file(
                self.private_key_file, self.key_passphrase
            )
            self.session.auth_publickey(self.username, key)
        else:
            key = DSSKey.from_private_key_file(
                self.private_key_file, self.key_passphrase
            )
            self.session.auth_publickey(self.username, key)

        self.channel = self.session.open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()
        if wait_prompt:
            self.receive()

    @property
    def connected(self):
        return bool(
            self.socket
            and not self.socket._closed
            and self.session
            and self.channel
        )

    def send(self, line, socket_timeout=None):
        socket_timeout = (
            socket_timeout
            if socket_timeout is not None
            else self.socket_timeout
        )
        self.channel.settimeout(socket_timeout)
        size = self.channel.sendall(line + "\n")
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

        self.channel.settimeout(socket_timeout)
        start = time()
        output = self.channel.recv(buffer_size).decode()
        LOG.debug(output)
        size = len(output)
        duration = time() - start
        while (
            not regex.search(output)
            and (timeout is None or duration < timeout)
            and size > 0
        ):
            data = self.channel.recv(buffer_size).decode()
            LOG.debug(data)
            size = len(data)
            output += data
            duration = time() - start

        if size < 0 and size != LIBSSH2_ERROR_EAGAIN:
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
        if self.session:
            self.session.close()

        if self.channel:
            self.channel.close()

        if self.socket:
            self.socket.close()

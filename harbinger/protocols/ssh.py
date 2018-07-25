from logging import getLogger
from select import select
from socket import socket, AF_INET, SOCK_STREAM
from time import time

from ssh2.session import Session

from harbinger.base.ssh import BaseSshConnection
from harbinger.exceptions import LIBSSH2_ERROR_EAGAIN
from harbinger.exceptions import (
    ReceiveTimeoutException,
    SocketTimeoutException,
    ReceiveException,
)

LOG = getLogger(__name__)


class SshConnection(BaseSshConnection):
    def connect(self, wait_prompt=True):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))
        self.session = Session()
        self.session.handshake(self.socket)
        if self.password is not None:
            self.session.userauth_password(self.username, self.password)
        else:
            self.session.userauth_publickey_fromfile(
                self.username,
                publickey=self.public_key_file,
                privatekey=self.private_key_file,
                passphrase=self.key_passphrase,
            )

        # use socket select instead
        self.channel = self.session.open_session()
        self.channel.pty()
        self.channel.shell()
        self.session.set_blocking(False)
        if wait_prompt:
            self.receive()

    @property
    def connected(self):
        return bool(
            self.socket
            and not self.socket._closed
            and self.session
            and self.channel
            and not self.channel.eof()
        )

    def send(self, line, socket_timeout=None):
        socket_timeout = (
            socket_timeout
            if socket_timeout is not None
            else self.socket_timeout
        )
        size = self.channel.write(line + "\n")
        select([], [self.socket], [], socket_timeout)
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

        start = time()
        # blocking = socket_timeout is not None
        # self.session.set_blocking(True)
        # if blocking:
        #     self.session.set_timeout(socket_timeout)
        select([self.socket], [], [], socket_timeout)
        size, data = self.channel.read()
        output = data.decode()
        LOG.debug(output)
        duration = time() - start
        while (
            not regex.search(output)
            and (timeout is None or duration < timeout)
            and size > 0
            and not self.channel.eof()
        ):
            select([self.socket], [], [], socket_timeout)
            size, data = self.channel.read()
            data = data.decode()
            LOG.debug(output)
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
        self.channel.close()
        self.channel.wait_closed()
        self.socket.close()

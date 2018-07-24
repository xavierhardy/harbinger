import re

from harbinger.base.connection import Connection

DEFAULT_BUFFER_SIZE = 4096


class ShellConnection(Connection):
    def __init__(self, hostname, port=22, username=None, password=None,
                 timeout=None, socket_timeout=None, prompt="^.*?@.*?(#|$) ",
                 buffer_size=DEFAULT_BUFFER_SIZE):
        super(ShellConnection, self).__init__(
            hostname=hostname, port=port, username=username, password=password,
            timeout=timeout,
        )

        assert isinstance(socket_timeout, (int, float)) or socket_timeout is None
        assert isinstance(buffer_size, int)
        assert isinstance(prompt, str)

        self.socket_timeout = socket_timeout
        self.buffer_size = buffer_size
        self.prompt = prompt
        self.prompt_regex = re.compile(prompt, re.I)

    def connect(self, wait_prompt=True):
        pass

    def send(self, line, socket_timeout=None):
        return 0

    def sanitize(self, output):
        return "\n".join(output.splitlines()[1:-1])

    def receive(self, regex=None, socket_timeout=None, timeout=None,
                buffer_size=DEFAULT_BUFFER_SIZE):
        return ""


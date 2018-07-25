import re
from io import DEFAULT_BUFFER_SIZE

from harbinger.base.shell import ShellConnection

GUESS_KEY_ALGORITHM = 0
DSA_KEY_ALGORITHM = 1
RSA_KEY_ALGORITHM = 2


class BaseSshConnection(ShellConnection):
    def __init__(
        self,
        hostname,
        port=22,
        username=None,
        password=None,
        timeout=None,
        socket_timeout=None,
        prompt="^.*?@.*?(#|$) ",
        buffer_size=DEFAULT_BUFFER_SIZE,
        public_key_file=None,
        private_key_file=None,
        key_passphrase="",
        key_algorithm=GUESS_KEY_ALGORITHM,
    ):
        super(BaseSshConnection, self).__init__(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            buffer_size=buffer_size,
        )

        assert isinstance(prompt, str)
        assert isinstance(public_key_file, str) or public_key_file is None
        assert isinstance(private_key_file, str) or private_key_file is None
        assert isinstance(key_passphrase, str)
        assert isinstance(key_algorithm, int) or 0 <= key_algorithm <= 2

        self.socket_timeout = socket_timeout
        self.prompt = prompt
        self.prompt_regex = re.compile(prompt, re.I)
        self.public_key_file = public_key_file
        self.private_key_file = private_key_file
        self.key_passphrase = key_passphrase
        self.key_algorithm = key_algorithm
        self.socket = None
        self.session = None
        self.channel = None

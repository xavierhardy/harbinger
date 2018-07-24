
class Connection(object):
    def __init__(self, hostname, port=None, username=None, password=None,
                 timeout=None):
        assert isinstance(hostname, str)
        assert isinstance(port, int) or port is None
        assert isinstance(username, str) or username is None
        assert isinstance(password, str) or password is None
        assert isinstance(timeout, (int, float)) or timeout is None

        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

    def connect(self):
        pass

    @property
    def connected(self):
        return False

    def send(self, line):
        return 0

    def receive(self):
        return ""

    def disconnect(self):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

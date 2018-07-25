
from ssh2.error_codes import *

LIBSSH2_ERROR_NAMES = {
    LIBSSH2CHANNEL_EAGAIN: "CHANNEL_EAGAIN",
    LIBSSH2_ERROR_AGENT_PROTOCOL: "AGENT_PROTOCOL",
    LIBSSH2_ERROR_AUTHENTICATION_FAILED: "AUTHENTICATION_FAILED",
    LIBSSH2_ERROR_BAD_SOCKET: "BAD_SOCKET",
    LIBSSH2_ERROR_BAD_USE: "BAD_USE",
    LIBSSH2_ERROR_BANNER_RECV: "BANNER_RECV",
    LIBSSH2_ERROR_BANNER_SEND: "BANNER_SEND",
    LIBSSH2_ERROR_BUFFER_TOO_SMALL: "BUFFER_TOO_SMALL",
    LIBSSH2_ERROR_CHANNEL_CLOSED: "CHANNEL_CLOSED",
    LIBSSH2_ERROR_CHANNEL_EOF_SENT: "CHANNEL_EOF_SENT",
    LIBSSH2_ERROR_CHANNEL_FAILURE: "CHANNEL_FAILURE",
    LIBSSH2_ERROR_CHANNEL_OUTOFORDER: "CHANNEL_OUTOFORDER",
    LIBSSH2_ERROR_CHANNEL_PACKET_EXCEEDED: "CHANNEL_PACKET_EXCEEDED",
    LIBSSH2_ERROR_CHANNEL_REQUEST_DENIED: "CHANNEL_REQUEST_DENIED",
    LIBSSH2_ERROR_CHANNEL_UNKNOWN: "CHANNEL_UNKNOWN",
    LIBSSH2_ERROR_CHANNEL_WINDOW_EXCEEDED: "CHANNEL_WINDOW_EXCEEDED",
    LIBSSH2_ERROR_COMPRESS: "COMPRESS",
    LIBSSH2_ERROR_DECRYPT: "DECRYPT",
    LIBSSH2_ERROR_EAGAIN: "EAGAIN",
    LIBSSH2_ERROR_ENCRYPT: "ENCRYPT",
    LIBSSH2_ERROR_FILE: "FILE",
    LIBSSH2_ERROR_HOSTKEY_INIT: "HOSTKEY_INIT",
    LIBSSH2_ERROR_HOSTKEY_SIGN: "HOSTKEY_SIGN",
    LIBSSH2_ERROR_INVAL: "INVAL",
    LIBSSH2_ERROR_INVALID_POLL_TYPE: "INVALID_POLL_TYPE",
    LIBSSH2_ERROR_KEY_EXCHANGE_FAILURE: "KEY_EXCHANGE_FAILURE",
    LIBSSH2_ERROR_KNOWN_HOSTS: "KNOWN_HOSTS",
    LIBSSH2_ERROR_METHOD_NONE: "METHOD_NONE",
    LIBSSH2_ERROR_METHOD_NOT_SUPPORTED: "METHOD_NOT_SUPPORTED",
    LIBSSH2_ERROR_NONE: "NONE",
    LIBSSH2_ERROR_OUT_OF_BOUNDARY: "OUT_OF_BOUNDARY",
    LIBSSH2_ERROR_PASSWORD_EXPIRED: "PASSWORD_EXPIRED",
    LIBSSH2_ERROR_PROTO: "PROTO",
    LIBSSH2_ERROR_PUBLICKEY_PROTOCOL: "PUBLICKEY_PROTOCOL",
    LIBSSH2_ERROR_PUBLICKEY_UNRECOGNIZED: "PUBLICKEY_UNRECOGNIZED",
    LIBSSH2_ERROR_PUBLICKEY_UNVERIFIED: "PUBLICKEY_UNVERIFIED",
    LIBSSH2_ERROR_REQUEST_DENIED: "REQUEST_DENIED",
    LIBSSH2_ERROR_SCP_PROTOCOL: "SCP_PROTOCOL",
    LIBSSH2_ERROR_SFTP_PROTOCOL: "SFTP_PROTOCOL",
    LIBSSH2_ERROR_SOCKET_DISCONNECT: "SOCKET_DISCONNECT",
    LIBSSH2_ERROR_SOCKET_NONE: "SOCKET_NONE",
    LIBSSH2_ERROR_SOCKET_RECV: "SOCKET_RECV",
    LIBSSH2_ERROR_SOCKET_TIMEOUT: "SOCKET_TIMEOUT",
    LIBSSH2_ERROR_TIMEOUT: "TIMEOUT",
    LIBSSH2_ERROR_ZLIB: "ZLIB",
}


class NetSshException(Exception):
    message = "Unknown harbinger Exception"

    def __str__(self):
        return self.message % vars(self)


class TimeoutException(NetSshException):
    message = "Unknown timeout Exception waiting for %(duration)ss with a " \
              "timeout of %(timeout)ss for '%(pattern)s': %(output)s"

    def __init__(self, output="", timeout=None, duration=0, pattern=""):
        self.output = output
        self.timeout = timeout
        self.duration = duration
        self.pattern = pattern


class ReceiveTimeoutException(TimeoutException):
    message = "Receive timeout waiting for %(duration)ss with a timeout of " \
              "%(timeout)ss for '%(pattern)s': pattern not found in %(output)s"


class SocketTimeoutException(TimeoutException):
    message = "Socket timeout waiting for %(duration)ss with a timeout of " \
              "%(timeout)ss for '%(pattern)s': nothing received in " \
              "%(timeout)ss, output: %(output)s"


class ReceiveException(NetSshException):
    message = "Exception %(error)s (code %(code)d) waiting for output for " \
              "%(duration)ss: %(output)s"

    def __init__(self, code=0, output="", duration=0):
        self.error = LIBSSH2_ERROR_NAMES.get(code, "unknown")
        self.code = code
        self.output = output
        self.duration = duration
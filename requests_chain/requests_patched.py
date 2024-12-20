
import urllib3, socks, six
from requests_chain import chained_socks
from requests_chain.chained_socks import custom_create_connection as custom_socks_create_connection

from urllib3.util.connection import allowed_gai_family, LocationParseError, socket, _set_socket_options



def custom_http_create_connection(
    conn,
    address,
    timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
    source_address=None,
    socket_options=None,
):
    """Connect to *address* and return the socket object.

    Convenience function.  Connect to *address* (a 2-tuple ``(host,
    port)``) and return the socket object.  Passing the optional
    *timeout* parameter will set the timeout on the socket instance
    before attempting to connect.  If no *timeout* is supplied, the
    global default timeout setting returned by :func:`socket.getdefaulttimeout`
    is used.  If *source_address* is set it must be a tuple of (host, port)
    for the socket to bind as a source address before making the connection.
    An host of '' or port 0 tells the OS to use the default.
    """

    host, port = address

    if host.startswith("["):
        host = host.strip("[]")
    err = None

    # Using the value from allowed_gai_family() in the context of getaddrinfo lets
    # us select whether to work with IPv4 DNS records, IPv6 records, or both.
    # The original create_connection function always returns all records.
    family = allowed_gai_family()

    try:
        host.encode("idna")
    except UnicodeError:
        return six.raise_from(
            LocationParseError(u"'%s', label empty or too long" % host), None
        )
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = conn

            # If provided, set socket level options before connecting.
            _set_socket_options(sock, socket_options)

            if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            if source_address:
                sock.bind(source_address)

            sock.connect(sa)
            return sock

        except socket.error as e:
            err = e
            if sock is not None:
                sock.close()
                sock = None

    if err is not None:
        raise err

    raise socket.error("getaddrinfo returns an empty list")

old_http_create_connection = urllib3.util.connection.create_connection
old_socks_create_connection = socks.create_connection


def patch_requests(conn):
    def http_create_connection(*args, **kwg):
        print("http_create_connection")
        res = custom_http_create_connection(conn, *args, **kwg)
        return conn

    def socks_create_connection(*args, **kwg):
        print("socks_create_connection")
        res = custom_socks_create_connection(conn, *args, **kwg)
        return res

    urllib3.util.connection.create_connection = http_create_connection
    socks.create_connection = socks_create_connection

    import sys
    del sys.modules['requests']
    sys.modules['requests'] = __import__('requests')   

def chain_requests(chain) -> chained_socks.socksocket:
  conn = chained_socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
  conn.setdefaultproxy() # Clear the default chain
  #adding hops with proxies
  for hop in chain:
      conn.adddefaultproxy(*chained_socks.parseproxy(hop))


  # Configure alternate routes (No proxy for localhost)
  conn.chain_setproxy('localhost', chained_socks.PROXY_TYPE_NONE)
  conn.chain_setproxy('127.0.0.1', chained_socks.PROXY_TYPE_NONE)

  patch_requests(conn)

  return conn






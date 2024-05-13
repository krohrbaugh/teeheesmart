from teeheesmart.constants import PROTOCOL_HEX
from teeheesmart.url_parser import Endpoint, parse_url, \
  _DEFAULT_HOST, _DEFAULT_PORT_TCP, _DEFAULT_PROTOCOL, \
  _DEFAULT_SCHEME

class TestEndpoint:
  # Scheme
  def test_sets_tcp_as_default_scheme(self):
    sut = Endpoint()

    assert sut.scheme == _DEFAULT_SCHEME

  def test_sets_scheme_as_specified(self):
    scheme = 'udp'

    sut = Endpoint(scheme = scheme)

    assert sut.scheme == scheme

  # Host
  def test_sets_host_default_when_not_specified(self):
    sut = Endpoint()

    assert sut.host == _DEFAULT_HOST

  def test_sets_host_as_specified(self):
    host = 'localhost'

    sut = Endpoint(host = host)

    assert sut.host == host

  # Port
  def test_sets_port_default_when_not_specified_and_tcp_scheme(self):
    sut = Endpoint()

    assert sut.port == _DEFAULT_PORT_TCP

  def test_leaves_port_unspecified_for_unknown_schemes(self):
    sut = Endpoint(scheme = 'udp')

    assert sut.port is None

  def test_sets_port_as_specified(self):
    port = 1337

    sut = Endpoint(port = port)

    assert sut.port == port

  # Protocol
  def test_sets_protocol_default_when_not_specified(self):
    sut = Endpoint()

    assert sut.protocol == _DEFAULT_PROTOCOL

  def test_sets_protocol_when_specified(self):
    protocol = 'http'

    sut = Endpoint(protocol = protocol)

    assert sut.protocol == protocol

class TestParseUrl:
  def test_host_only_parses_correctly(self):
    url = 'localhost'

    result = parse_url(url)

    assert result.scheme == _DEFAULT_SCHEME
    assert result.host == url
    assert result.port == _DEFAULT_PORT_TCP
    assert result.protocol == _DEFAULT_PROTOCOL

  def test_host_and_port_only_parses_correctly(self):
    host = '10.0.0.1'
    port = 1337
    url = f'{host}:{port}'

    result = parse_url(url)

    assert result.scheme == _DEFAULT_SCHEME
    assert result.host == host
    assert result.port == port
    assert result.protocol == _DEFAULT_PROTOCOL

  def test_scheme_and_host_parses_correctly(self):
    scheme = 'udp'
    host = '192.168.0.1'
    url = f'{scheme}://{host}'

    result = parse_url(url)

    assert result.scheme == scheme
    assert result.host == host
    assert result.port is None
    assert result.protocol == _DEFAULT_PROTOCOL

  def test_scheme_host_and_port_parses_correctly(self):
    scheme = 'udp'
    host = '192.168.0.1'
    port = 50000
    url = f'{scheme}://{host}:{port}'

    result = parse_url(url)

    assert result.scheme == scheme
    assert result.host == host
    assert result.port == port
    assert result.protocol == _DEFAULT_PROTOCOL

  def test_scheme_host_port_and_protocol_parses_correctly(self):
    scheme = 'http'
    host = 'mediaswitch.local'
    port = 1337
    protocol = 'l33tsp34k'
    url = f'{scheme}://{host}:{port}#{protocol}'

    result = parse_url(url)

    assert result.scheme == scheme
    assert result.host == host
    assert result.port == port
    assert result.protocol == protocol

  def test_host_and_protocol_parses_correctly(self):
    host = 'mediaswitch.local'
    protocol = 'l33tsp34k'
    url = f'{host}#{protocol}'

    result = parse_url(url)

    assert result.scheme == _DEFAULT_SCHEME
    assert result.host == host
    assert result.port == _DEFAULT_PORT_TCP
    assert result.protocol == protocol

  def test_host_port_and_protocol_parses_correctly(self):
    host = 'mediaswitch.local'
    protocol = 'l33tsp34k'
    port = 1337
    url = f'{host}:{port}#{protocol}'

    result = parse_url(url)

    assert result.scheme == _DEFAULT_SCHEME
    assert result.host == host
    assert result.port == port
    assert result.protocol == protocol

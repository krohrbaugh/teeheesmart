"""TESmart HDMI switch control library"""
from typing import Optional

from .constants import PROTOCOL_HEX, SCHEME_TCP
from .url_parser import parse_url
from .media_switch import MediaSwitch

from .hex import get_tcp_media_switch

def get_media_switch(
    url: str,
    timeout_sec: Optional[float] = None
  ) -> MediaSwitch:
  """
  Create media switch representation whose state can be accessed via the specified
  URL.

  Currently supported:
    + Schemes:
      + TCP (identifier: tcp)
    + Protocols:
      + Hex (identifier: hex)

  Defaults:
    + Default scheme: TCP (identifier: tcp)
    + Default TCP port: 5000
    + Default protocol: Hex (identifier: hex)

  URL format:
    The URL takes the form of `<scheme>://<host>:<port>#<protocol>` with all
    but the host being optional.

    Examples:
      + 10.0.0.1 ->
          Scheme: tcp, Host: 10.0.0.1, Port: 5000, Protocol: hex 
      + localhost:1337 ->
          Scheme: tcp, Host: localhost, Port: 1337, Protocol: hex 
      + localhost:1337#hex->
          Scheme: tcp, Host: localhost, Port: 1337, Protocol: hex 
      + tcp://10.0.0.1 ->
          Scheme: tcp, Host: 10.0.0.1, Port: 5000, Protocol: hex
      + tcp://switch.local:8080 ->
          Scheme: tcp, Host: switch.local, Port: 8080, Protocol: hex
      + tcp://localhost:8080#hex
          Scheme: tcp, Host: localhost, Port: 8080, Protocol: hex

  Args:
    url (str): The URL at which the device state can be accessed.
    timeout_sec (Optional[float]): Timeout, in seconds, to use when communicating
      with the device. Default: None, which allows the underlying protocol driver
      to determine.

  Returns:
    MediaSwitch: Representation of the media switch device, including methods for
      controlling it (e.g., selecting sources.)
  """
  endpoint = parse_url(url)
  if endpoint.protocol == PROTOCOL_HEX and endpoint.scheme == SCHEME_TCP:
    return get_tcp_media_switch(
      host = endpoint.host,
      port = endpoint.port,
      timeout_sec = timeout_sec,
    )
  else:
    raise ValueError(f'Unsupported url specified: {url}')
  
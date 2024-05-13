from typing import Optional
from urllib.parse import urlparse

from .constants import PROTOCOL_HEX, SCHEME_TCP

_DEFAULT_HOST = 'localhost'
_DEFAULT_PORT_TCP = 5000
_DEFAULT_PROTOCOL = PROTOCOL_HEX
_DEFAULT_SCHEME = SCHEME_TCP

def _is_empty(value: str) -> bool:
  return (value is None or len(value) == 0)


class Endpoint:
  def __init__(
      self,
      scheme: Optional[str] = None,
      host: Optional[str] = None,
      port:Optional[int] = None,
      protocol: Optional[str] = None
    ):
    if _is_empty(scheme):
      self._scheme = _DEFAULT_SCHEME
    else:
      self._scheme = scheme

    if _is_empty(host):
      self._host = _DEFAULT_HOST
    else:
      self._host = host

    if port is None:
      self._port = self._default_port(self._scheme)
    else:
      self._port = port

    if _is_empty(protocol):
      self._protocol = _DEFAULT_PROTOCOL
    else:
      self._protocol = protocol

  @property
  def scheme(self):
    return self._scheme

  @property
  def host(self):
    return self._host

  @property
  def port(self):
    return self._port

  @property
  def protocol(self):
    return self._protocol

  def _default_port(self, scheme: str) -> Optional[int]:
    if scheme == SCHEME_TCP:
      return _DEFAULT_PORT_TCP
    return None


def parse_url(url: str) -> Endpoint:
  normalized_url = url
  if '://' not in url:
    normalized_url = f'{_DEFAULT_SCHEME}://{url}'
  parsed_url = urlparse(normalized_url)
  endpoint = Endpoint(
    scheme = parsed_url.scheme,
    host = parsed_url.hostname,
    port = parsed_url.port,
    protocol = parsed_url.fragment
  )
  return endpoint

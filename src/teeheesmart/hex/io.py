import itertools
import socket

from ..constants import LOGGER
from enum import IntEnum, unique
from typing import Optional


@unique
class Command(IntEnum):
  """
  Enumerates the supported Hex commands
  """
  # See https://support.tesmart.com/hc/en-us/article_attachments/27716605047961 for command documentation
  NULL_RESPONSE = 0
  SWITCH_VIDEO = 1
  MUTE_BUZZER = 2
  LED_TIMEOUT_SECONDS =  3
  QUERY_ACTIVE_INPUT = 16
  CURRENT_ACTIVE_INPUT = 17
  ENABLE_INPUT_DETECTION = 129

  @classmethod
  def is_supported(cls, cmd_id: int) -> bool:
    return cmd_id in iter(Command)

# Validation rules: limit I/O values to one byte
_VALUE_MIN = 0
_VALUE_MAX = 255 # Only 8 bits available for data transport
_VALID_RANGE: range = range(_VALUE_MIN, _VALUE_MAX)
  
def _validated_value(maybe_value: Optional[int], default_value: int = 0) -> int:
  if maybe_value is None:
    return default_value
  if maybe_value not in _VALID_RANGE:
    raise ValueError(
      f'Valid values are between {_VALUE_MIN} and {_VALUE_MAX - 1}, '
      f'inclusive. Received: {maybe_value}'
    )
  else:
    return maybe_value

class Instruction:
  """
  Encapsulates a fully-formed Hex instruction
  """

  # Default name for unsupported/unrecognized commands
  UNSUPPORTED_COMMAND_NAME: str = "UNSUPPORTED"

  # Hex uses 6-byte instructions
  SIZE_BYTES: int = 6

  def __init__(
    self,
    cmd: int,
    data_value: Optional[int] = None
  ):
    if Command.is_supported(cmd):
      self._command = Command(cmd)
      self._unsupported_command_id = None
    else:
      self._command = None
      self._unsupported_command_id = cmd

    self._data_value = _validated_value(data_value)
    
  @property
  def id(self) -> int:
    if self._command is not None:
      return self._command.value
    else:
      return self._unsupported_command_id

  @property
  def name(self) -> str:
    if self._command is not None:
      return self._command.name
    else:
      return Instruction.UNSUPPORTED_COMMAND_NAME

  @property
  def data_value(self) -> int:
    return self._data_value

  @property
  def is_supported(self) -> bool:
    return self._command is not None

  @property
  def frame(self) -> list[int]:
    return [
      0xAA,
      0xBB,
      0x03,
      self.id,
      self.data_value,
      0xEE
    ]

  def __str__(self) -> str:
    return (
      f'<Instruction id: {self.id} name: {self.name} data_value: {self.data_value}>'
    )

  def __repr__(self) -> str:
    return (
      f'Instruction<{self.name}>({self.id}, {self.data_value})'
    )

  def __eq__(self, other):
    if not isinstance(other, Instruction):
      return NotImplemented
    return self.frame == other.frame

class Codec:
  """
  Bidirectionally converts between Instruction and bytes
  """

  @classmethod
  def encode(cls, instruction: Instruction) -> bytes:
    msg = cls._encode_message(instruction)
    data = bytes(msg)
    return data
  
  @classmethod
  def decode(cls, data: bytes) -> Instruction:
    frame = cls._decode_message(data)
    cmd = Instruction(*frame)
    return cmd

  @classmethod
  def _encode_message(cls, instruction: Instruction) -> list[int]:
    return instruction.frame
  
  @classmethod
  def _decode_message(cls, data: bytes) -> list[int]:
    _, _, _, cmd_id, data_value, _ = [byte for byte in data]
    return [cmd_id, data_value]

class TcpEndpoint:
  """
  Hex Protocol TCP endpoint location details
  """
  DEFAULT_PORT: int = 5000
  DEFAULT_TIMEOUT_SEC: float = 0.250

  def __init__(
      self,
      host: str,
      port: Optional[int] = None,
      timeout_sec: Optional[float] = DEFAULT_TIMEOUT_SEC
    ):
    self._host = host
    if port is None:
      self._port = TcpEndpoint.DEFAULT_PORT
    else:
      self._port = port
    self._timeout_sec = timeout_sec

  @property
  def host(self) -> str:
    return self._host

  @property
  def port(self) -> int:
    return self._port

  @property
  def timeout_sec(self) -> Optional[float]:
    return self._timeout_sec

class TcpDevice:
  """
  Manages TCP I/O for a specific Hex Protocol-based device
  """

  def __init__(
      self,
      endpoint: TcpEndpoint,
    ):
    self._endpoint = endpoint

  def process(self, instructions: list[Instruction] | Instruction) -> list[Instruction]:
    try:
      _ = iter(instructions)
    except TypeError:
      # Single instruction provided; wrap it.
      instructions = [instructions]
    results = []

    conn = self._create_connection()
    try:
      for instruction in instructions:
        result = self._execute_instruction(instruction, conn)
        results.append(result)
    except Exception as ex:
      LOGGER.error('Failed communicating with device: %s', ex)
    finally:
      conn.close()

    # Results is a list of lists, so flatten before returning
    flat_results = list(itertools.chain.from_iterable(results))
    return flat_results
  
  def _create_connection(self) -> socket.socket:
    conn = socket.create_connection(
      (self._endpoint.host, self._endpoint.port)
    )
    conn.settimeout(self._endpoint.timeout_sec)
    return conn
  
  def _execute_instruction(
      self,
      instruction: Instruction,
      conn: socket.socket
    ) -> list[Instruction]:
    req_bytes = Codec.encode(instruction)
    conn.send(req_bytes)

    # Device either returns a single instruction specifying the selected input
    # or no response at all.
    result: list[Instruction] = []
    chunks: list[bytes] = []
    bytes_received = 0
    try:
      while bytes_received < Instruction.SIZE_BYTES:
        chunk = conn.recv(min(Instruction.SIZE_BYTES - bytes_received, Instruction.SIZE_BYTES))
        if chunk == b'':
          instruction = Instruction(Command.NULL_RESPONSE)
          result.append(instruction)
          break
        else:
          chunks.append(chunk)
          bytes_received = bytes_received + len(chunk)

      if bytes_received == Instruction.SIZE_BYTES:
        resp_bytes = b''.join(chunks)
        instruction = Codec.decode(resp_bytes)
        result.append(instruction)
    except TimeoutError:
      LOGGER.info(
        'Timed out waiting for response. Ignoring, since device does not always send '
        'a response.'
      )

    return result

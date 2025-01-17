from ..constants import LOGGER
from ..media_switch import MediaSwitch as MediaSwitchProtocol
from .io import Command, Instruction, TcpDevice

MAX_SUPPORTED_INPUTS = 16

class MediaSwitch(MediaSwitchProtocol):
  def __init__(self, device: TcpDevice):
    self._device = device 
    self._selected_source = 0
    self._input_count = 0
    self._output_count = 1 # Matrix switches not currently supported
    self.update()
    self._determine_input_count()

  def select_source(self, input: int) -> None:
    """
    Select the specified video input
    """
    normalized_input = input
    if normalized_input < 1:
      normalized_input = 1
    elif self.input_count > 0 and normalized_input > self.input_count:
      normalized_input = self.input_count

    instruction = Instruction(Command.SWITCH_VIDEO, normalized_input)
    self._process(instruction)

  def set_buzzer_muting(self, mute_buzzer: bool) -> None:
    """
    Enable or disable the buzzer
    """
    instruction = Instruction(Command.MUTE_BUZZER, not mute_buzzer)
    self._process(instruction)

  def set_led_timeout_seconds(self, led_timeout_seconds: int) -> None:
    """
    Set the LED timeout
    """
    normalized_timeout = led_timeout_seconds
    if normalized_timeout not in [0, 10, 30]:
      normalized_timeout = 0
    instruction = Instruction(Command.LED_TIMEOUT_SECONDS, normalized_timeout)
    self._process(instruction)

  def set_auto_input_detection(self, enable_auto_input_detection: bool) -> None:
    """
    Enable or disable input auto-detection
    """
    instruction = Instruction(Command.ENABLE_INPUT_DETECTION, enable_auto_input_detection)
    self._process(instruction)

  def update(self) -> None:
    self._process(self._update_instructions())

  @property
  def selected_source(self) -> int:
    """
    Returns the input number of the selected source
    """
    return self._selected_source

  @property
  def input_count(self) -> int:
    """
    The number of inputs the switch has
    """
    return self._input_count

  @property
  def output_count(self) -> int:
    """
    The number of outputs the switch has
    """
    return self._output_count

  def _process(self, instructions: list[Instruction] | Instruction) -> None:
    results = self._device.process(instructions)
    self._update_from_instructions(results)

  def _update_from_instructions(self, instructions: list[Instruction]) -> None:
    for instruction in instructions:
      match instruction.id:
        case Command.CURRENT_ACTIVE_INPUT:
          self._selected_source = instruction.data_value + 1
        case _:
          LOGGER.info('Discarded instruction: %s', instruction)

  def _determine_input_count(self) -> None:
    # Determine current selected input
    prev_selected_source = self.selected_source
    self._selected_source = 0

    # Determine highest valid source by selecting them and seeing if it was valid
    for input in range(MAX_SUPPORTED_INPUTS, 0, -1):
      self.select_source(input)
      if (self.selected_source != 0):
        self._input_count = self.selected_source
        break

    # Restore previously selected input
    self.select_source(prev_selected_source)
  
  def _update_instructions(self) -> list[Instruction]:
    return [
      # Queries the currently selected input
      Instruction(Command.QUERY_ACTIVE_INPUT)
    ]

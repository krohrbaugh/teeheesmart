from typing import Protocol

class MediaSwitch(Protocol):
  """
  Representation of a multi-input, single- or fixed-output media switch, such as a
  16x1 HDMI switch.

  Example TESmart devices: HSW1601, HSW801
  """

  def select_source(self, input: int) -> None:
    """
    Select the specified video input
    """

  def set_buzzer_muting(self, mute_buzzer: bool) -> None:
    """
    Enable or disable the buzzer
    """

  def set_led_timeout_seconds(self, led_timeout_seconds: int) -> None:
    """
    Set the LED timeout
    """

  def set_auto_input_detection(self, enable_auto_input_detection: bool) -> None:
    """
    Enable or disable input auto-detection
    """

  def update(self) -> None:
    """
    Refresh device state.
    """

  @property
  def selected_source(self) -> int:
    """
    Returns the input number of the selected source
    """

  @property
  def input_count(self) -> int:
    """
    Returns the number of inputs the switch has
    """

  @property
  def output_count(self) -> int:
    """
    Returns the number of outputs the switch has
    """

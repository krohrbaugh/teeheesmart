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

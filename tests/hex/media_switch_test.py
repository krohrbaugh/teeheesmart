from typing import Optional

from teeheesmart.hex.io import Command, Instruction
from teeheesmart.hex.media_switch import MediaSwitch

from fakes import FakeDevice

class TestMediaSwitch:
  def test_initializes_state_from_device(self):
    input_count = 14
    output_count = 1
    selected_source = 3
    fake_device = FakeDevice()
    response_instructions = [
      [Instruction(Command.CURRENT_ACTIVE_INPUT, selected_source - 1)],
      [], # SWITCH_VIDEO: 16
      [], # SWITCH_VIDEO: 15
      [Instruction(Command.CURRENT_ACTIVE_INPUT, input_count - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, selected_source - 1)]
    ]
    fake_device.response_instructions = response_instructions

    (sut, _) = self.create_media_switch(device = fake_device)

    assert sut.input_count == input_count
    assert sut.output_count == output_count
    assert sut.selected_source == selected_source

  def test_update_reloads_state_from_device(self):
    input_count = 16
    output_count = 1
    selected_source = 3
    selected_source2 = 12
    fake_device = FakeDevice()
    response_instructions = [
      [Instruction(Command.CURRENT_ACTIVE_INPUT, selected_source - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, input_count - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, selected_source - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, selected_source2 - 1)],
    ]
    fake_device.response_instructions = response_instructions

    (sut, _) = self.create_media_switch(device = fake_device)

    assert sut.input_count == input_count
    assert sut.output_count == output_count
    assert sut.selected_source == selected_source

    # Device state changed
    sut.update()

    assert sut.input_count == input_count
    assert sut.output_count == output_count
    assert sut.selected_source == selected_source2

  def test_selected_source_sends_switch_video_instruction(self):
    input_count = 16
    selected_source = 3
    fake_device = FakeDevice()
    response_instructions = [
      [Instruction(Command.CURRENT_ACTIVE_INPUT, selected_source - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, input_count - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, selected_source - 1)],
    ]
    expected = [Instruction(Command.SWITCH_VIDEO, selected_source)]
    fake_device.response_instructions = response_instructions

    (sut, _) = self.create_media_switch(device = fake_device)
    fake_device.clear_instructions()

    sut.select_source(selected_source)

    assert sut.selected_source == selected_source
    assert fake_device.processed_instructions == expected

  def test_selected_source_normalizes_negative_value_to_1(self):
    input_count = 8
    selected_source = -5
    expected_source = 1
    fake_device = FakeDevice()
    response_instructions = [
      [Instruction(Command.CURRENT_ACTIVE_INPUT, expected_source - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, input_count - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, expected_source - 1)],
    ]
    expected = [Instruction(Command.SWITCH_VIDEO, expected_source)]
    fake_device.response_instructions = response_instructions

    (sut, _) = self.create_media_switch(device = fake_device)
    fake_device.clear_instructions()

    sut.select_source(selected_source)

    assert sut.selected_source == expected_source
    assert fake_device.processed_instructions == expected

  def test_selected_source_normalizes_sources_above_max_to_last_input(self):
    input_count = 16
    initial_source = 3
    selected_source = 17
    expected_source = 16
    fake_device = FakeDevice()
    response_instructions = [
      [Instruction(Command.CURRENT_ACTIVE_INPUT, initial_source - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, input_count - 1)],
      [Instruction(Command.CURRENT_ACTIVE_INPUT, initial_source - 1)],
    ]
    expected = [Instruction(Command.SWITCH_VIDEO, expected_source)]
    fake_device.response_instructions = response_instructions

    (sut, _) = self.create_media_switch(device = fake_device)
    fake_device.clear_instructions()
    fake_device.response_instructions = [
      [Instruction(Command.CURRENT_ACTIVE_INPUT, expected_source - 1)],
    ]

    sut.select_source(selected_source)

    assert sut.selected_source == expected_source
    assert fake_device.processed_instructions == expected

  def create_media_switch(
      self,
      device = FakeDevice()
    ) -> tuple[MediaSwitch, FakeDevice]:
    return (MediaSwitch(device), device)


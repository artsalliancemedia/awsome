from AWSome.command import AWSCommand
from AWSome.loader.yaml import YamlLoader

import pytest

from tests.fixtures import options
from tests.fixtures.yaml import broken_yaml
from tests.fixtures.yaml import commands_not_a_list
from tests.fixtures.yaml import commands_not_dicts
from tests.fixtures.yaml import commands_too_many_dicts
from tests.fixtures.yaml import commands_with_wrong_format
from tests.fixtures.yaml import commands_with_wrong_values
from tests.fixtures.yaml import list_vpcs
from tests.fixtures.yaml import no_commands
from tests.fixtures.yaml import yaml_list


def test_commands_are_dictionaries(commands_not_dicts, options):
  loader = YamlLoader(options)
  pytest.raises(Exception, loader.load, commands_not_dicts)


def test_commands_dictionaries_have_one_key(commands_too_many_dicts, options):
  loader = YamlLoader(options)
  pytest.raises(Exception, loader.load, commands_too_many_dicts)


def test_command_is_built(list_vpcs, options):
  loader = YamlLoader(options)
  commands = loader.load(list_vpcs)
  assert len(commands) == 1

  formatted = commands[0].format()
  assert formatted == "aws ec2 describe-vpcs"


def test_commands_keys_are_commands(commands_with_wrong_format, options):
  loader = YamlLoader(options)
  pytest.raises(Exception, loader.load, commands_with_wrong_format)


def test_commands_values_are_dicts_or_none(commands_with_wrong_values, options):
  loader = YamlLoader(options)
  pytest.raises(Exception, loader.load, commands_with_wrong_values)


def test_file_fails_to_parse(broken_yaml, options):
  loader = YamlLoader(options)
  pytest.raises(Exception, loader.load, broken_yaml)


def test_non_objects_are_rejected(yaml_list, options):
  loader = YamlLoader(options)
  pytest.raises(Exception, loader.load, yaml_list)


def test_objects_commands_is_a_list(commands_not_a_list, options):
  loader = YamlLoader(options)
  pytest.raises(Exception, loader.load, commands_not_a_list)


def test_objects_need_commands_key(no_commands, options):
  loader = YamlLoader(options)
  pytest.raises(Exception, loader.load, no_commands)


def test_returns_a_list_of_commands(list_vpcs, options):
  loader = YamlLoader(options)
  commands = loader.load(list_vpcs)
  assert isinstance(commands, list)
  for command in commands:
    assert isinstance(command, AWSCommand)

from AWSome.loader.factory import get_loader

import pytest

from tests.fixtures import options
from tests.fixtures.profile import yaml_config
from tests.fixtures.profile import yaml_profile
from tests.fixtures.profile import yaml_profile_empty


def test_nested_variables_are_expanded(options, yaml_profile):
  options.profile = yaml_profile
  loader = get_loader(options)
  commands = loader.loads("commands:\n  - a: { group: {{ group.ci.test }} }")
  cmd = commands[0].format()
  assert cmd == 'aws a --group="b"'


def test_profile_is_used_to_expand(options, yaml_config, yaml_profile):
  options.profile = yaml_profile
  loader = get_loader(options)
  commands = loader.load(yaml_config)
  cmd = commands[0].format()
  assert cmd == 'aws a --vpc-id="a"'


def test_parser_fails_if_var_is_not_defined(options, yaml_config, yaml_profile_empty):
  options.profile = yaml_profile_empty
  loader = get_loader(options)
  pytest.raises(Exception, loader.load, yaml_config)

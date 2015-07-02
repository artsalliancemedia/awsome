import pytest

from tests.fixtures import stub_file


@pytest.fixture
def broken_yaml(request):
  """A corrupted YAML file"""
  return stub_file(request, "abc: -")


@pytest.fixture
def commands_not_a_list(request):
  """A YAML dict without the commands key"""
  return stub_file(request, "commands:\n  a: b")


@pytest.fixture
def commands_not_dicts(request):
  """A YAML dict with commands list not dicts"""
  return stub_file(request, "commands:\n  - a")


@pytest.fixture
def commands_too_many_dicts(request):
  """A YAML dict with commands list of more than one dict"""
  return stub_file(request, "commands:\n  - a: b\n    c: d")


@pytest.fixture
def commands_with_wrong_format(request):
  """A YAML dict with commands list but not all commands are valid."""
  return stub_file(
      request,
      "commands:\n  - ec2: ~\n  - ec2 describe-vpcs: ~\n"
      "  - not a valid format: ~"
  )


@pytest.fixture
def commands_with_wrong_values(request):
  """A YAML dict with commands list but not all options are valid."""
  return stub_file(
      request, "commands:\n  - ec2: ~\n  - ec2 describe-vpcs: a"
  )


@pytest.fixture
def list_vpcs(request):
  """A YAML file with the VPC listing command"""
  return stub_file(request, "commands:\n  - ec2 describe-vpcs: ~")


@pytest.fixture
def no_commands(request):
  """A YAML dict without the commands key"""
  return stub_file(request, "a: b\nc: d")


@pytest.fixture
def yaml_list(request):
  """A YAML file with a list in it"""
  return stub_file(request, "- a\n- b")

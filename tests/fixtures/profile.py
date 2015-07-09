import pytest

from tests.fixtures import stub_file


@pytest.fixture
def yaml_config(request):
  return stub_file(request, "commands:\n  - a:\n      vpc-id: {{ vpc }}")


@pytest.fixture
def yaml_profile(request):
  return stub_file(request, "# A comment\nvpc: a\ngroup: { ci: { test: b } }")


@pytest.fixture
def yaml_profile_empty(request):
  return stub_file(request, "")

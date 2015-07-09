from AWSome.executor import Executor
from AWSome.extentions.update_profile import UpdateProfile

import pytest

from tests.fixtures import options
from tests.fixtures.profile import yaml_profile


class MockCommand(object):
  def __init__(self, profile=None):
    self.extentions = { "update-profile": profile or {} }


class TestUpdateProfileConfig(object):
  def test_raises_if_profile_is_missing(self, options):
    command = MockCommand()
    executor = Executor("echo")
    extention = UpdateProfile(options)
    pytest.raises(Exception, extention.post_run, command, executor)

  def test_raises_if_update_from_is_missing(self, options):
    options.profile = "abc"
    command = MockCommand({ "key": "a" })
    executor = Executor("echo")
    extention = UpdateProfile(options)
    pytest.raises(Exception, extention.post_run, command, executor)

  def test_raises_if_update_key_is_missing(self, options):
    options.profile = "abc"
    command = MockCommand({ "option": 1 })
    executor = Executor("echo")
    extention = UpdateProfile(options)
    pytest.raises(Exception, extention.post_run, command, executor)

  def test_returns_if_update_config_is_missing(self, options):
    options.profile = "abc"
    command = MockCommand()
    executor = Executor("echo")
    extention = UpdateProfile(options)
    reload_conf = extention.post_run(command, executor)
    assert reload_conf == False


class TestUpdateProfileJSON(object):
  def test_raises_if_json_is_not_dict(self, options):
    options.profile = "abc"
    command = MockCommand({ "key": "a", "from": "b" })
    executor = Executor("echo")
    executor._stdout = "[]".encode("utf8")
    extention = UpdateProfile(options)
    pytest.raises(Exception, extention.post_run, command, executor)

  def test_raises_if_from_is_not_in_json(self, options):
    options.profile = "abc"
    command = MockCommand({ "key": "a.b.c", "from": "d" })
    executor = Executor("echo")
    executor._stdout = '{"a": { "b": 2 }}'.encode("utf8")
    extention = UpdateProfile(options)
    pytest.raises(Exception, extention.post_run, command, executor)

  def test_raises_if_output_is_no_json(self, options):
    options.profile = "abc"
    command = MockCommand({ "key": "a", "from": "b" })
    executor = Executor("echo")
    executor._stdout = "".encode("utf8")
    extention = UpdateProfile(options)
    pytest.raises(Exception, extention.post_run, command, executor)


class TestUpdateProfileYAML(object):
  def test_key_is_created_if_possible(self, yaml_profile):
    options.profile = yaml_profile
    command = MockCommand({ "key": "group.test.b", "from": "b" })
    executor = Executor("echo")
    executor._stdout = '{ "b": 2 }'.encode("utf8")
    extention = UpdateProfile(options)
    reload_conf = extention.post_run(command, executor)
    assert reload_conf

  def test_profile_is_updated(self, yaml_profile):
    options.profile = yaml_profile
    command = MockCommand({ "key": "group.test.b", "from": "b" })
    executor = Executor("echo")
    executor._stdout = '{ "b": 2 }'.encode("utf8")

    extention = UpdateProfile(options)
    reload_conf = extention.post_run(command, executor)
    profile_file = open(yaml_profile)
    profile = profile_file.read()
    assert profile == (
        "# A comment\n"
        "vpc: a\n"
        "group: {ci: {test: b}, test: {b: 2}}\n"
    )

  def test_raises_if_key_is_missing_and_cannot_be_created(self, yaml_profile):
    options.profile = yaml_profile
    command = MockCommand({ "key": "vpc.test", "from": "b" })
    executor = Executor("echo")
    executor._stdout = '{ "b": 2 }'.encode("utf8")
    extention = UpdateProfile(options)
    pytest.raises(Exception, extention.post_run, command, executor)

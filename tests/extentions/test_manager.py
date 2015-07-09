from AWSome.executor import Executor
from AWSome.extentions import Extention
from AWSome.extentions import SkipException
from AWSome.extentions.manager import ExtentionsManager

import pytest

from tests.fixtures import options


class MockCommand(object):
  def __init__(self):
    self.extentions = { "update-profile": {} }


class MockExtention(Extention):
  def __init__(self, options, exc_class=None):
    super(MockExtention, self).__init__(options)
    self._exc_class = exc_class

  def post_run(self, command, executor):
    if self._exc_class:
      raise self._exc_class("test")


class TestExtentionsManager(object):
  def test_extentions_are_loaded(self, options):
    ExtentionsManager.EXTENTIONS = { "update-profile": MockExtention }

    command = MockCommand()
    executor = Executor("echo")
    extentions = ExtentionsManager(options)

    extentions.post_run(command, executor)
    assert extentions._loaded_extentions != {}

  def test_exceptions_are_propagated(self):
    ExtentionsManager.EXTENTIONS = {
        "update-profile": lambda o: MockExtention(o, Exception)
    }

    command = MockCommand()
    executor = Executor("echo")
    extentions = ExtentionsManager(options)
    pytest.raises(Exception, extentions.post_run, command, executor)

  def test_skip_exceptions_are_not_propagated(self):
    ExtentionsManager.EXTENTIONS = {
        "update-profile": lambda o: MockExtention(o, SkipException)
    }

    command = MockCommand()
    executor = Executor("echo")
    extentions = ExtentionsManager(options)

    reload_conf = extentions.post_run(command, executor)
    assert reload_conf == False

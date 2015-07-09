from AWSome.executor import Executor
from AWSome.extentions import Extention
from AWSome.extentions.manager import ExtentionsManager

from tests.fixtures import options


class MockCommand(object):
  def __init__(self):
    self.extentions = { "update-profile": {} }


class MockExtention(Extention):
  def post_run(self, command, executor):
    pass


class TestExtentionsManager(object):
  def test_extentions_are_loaded(self, options):
    ExtentionsManager.EXTENTIONS = { "update-profile": MockExtention }

    command = MockCommand()
    executor = Executor("echo")
    extentions = ExtentionsManager(options)

    extentions.post_run(command, executor)
    assert extentions._loaded_extentions != {}

from abc import ABCMeta
from abc import abstractmethod


class Extention(metaclass=ABCMeta):
  """Abstract extention definiton.
  Extentions are collections of hooks that are run at registered points.
  """
  def __init__(self, options):
    self._options = options

  @abstractmethod
  def post_run(self, command, executor):
    pass


class SkipException(Exception):
  pass

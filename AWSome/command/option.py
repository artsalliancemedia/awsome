from abc import ABCMeta
from abc import abstractmethod


class CommandOption(metaclass=ABCMeta):
  """Base class to store options for the generated command."""
  def __init__(self, name, value):
    self._name = name
    self._value = value

  @abstractmethod
  def format(self):
    """Formats the option stored by this instance."""
    pass


class BoolOption(CommandOption):
  def format(self):
    prefix = "" if self._value else "no-"
    return "--{0}{1}".format(prefix, self._name)


class ListOption(CommandOption):
  def format(self):
    escaped = [
        '"{0}"'.format(value.replace('"', '\\"'))
        for value in self._value
    ]
    return "--{0} {1}".format(self._name, ' '.join(escaped))


class LiteralOption(CommandOption):
  def format(self):
    return self._value


class StringOption(CommandOption):
  def format(self):
    value = self._value.replace('"', '\\"')
    return '--{0}="{1}"'.format(self._name, value)

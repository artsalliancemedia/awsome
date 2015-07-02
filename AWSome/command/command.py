from AWSome.command.option import BoolOption
from AWSome.command.option import ListOption
from AWSome.command.option import StringOption


class AWSCommand(object):
  """Represents an AWS command to generate."""
  @staticmethod
  def get_option(name, value):
    """
    Converts the given option name and value pair into a CommandOption.

    :param str name: The name of the option.
    :param value: The value of the option.
                  The type of this value is used to determine the kind of
                  CommandOption to return.
    :returns: A CommandOption.
    """
    if isinstance(value, bool):
      return BoolOption(name, value)

    if isinstance(value, list):
      return ListOption(name, value)

    return StringOption(name, str(value))

  def __init__(self, command, globals=None, options=None, subcommand=None):
    """Creates a aws command representation.
    :param str command: The command to execute.
    :param [CommandOption] globals: The global options to set, if any.
    :param [CommandOption] options: The options for the [sub-]command.
    :param str subcommand: The sub-command to execute.
    """
    self._command = command
    self._globals = globals or []
    self._options = options or []
    self._subcommand = subcommand

  def format(self):
    """Formats the command into a string the user can run."""
    parts = ["aws"]

    # Append global options.
    for option in self._globals:
      parts.append(option.format())

    # Append command and subcommand.
    parts.append(self._command)
    if self._subcommand:
      parts.append(self._subcommand)

    # Append command options.
    for option in self._options:
      parts.append(option.format())

    return " ".join(parts)

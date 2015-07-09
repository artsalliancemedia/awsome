import yaml

from AWSome.command import AWSCommand
from AWSome.loader import Loader


class YamlLoader(Loader):
  """Loads a YAML file into an AWSCommand.

  The format of YAML files is as follows:

    # Global options.
    option1: value
    option2: value
    # ...

    # Commands are executed in the order they are defined.
    commands:
      - command1 subcommand1: ~
      - command1 subcommand2: ~
      - command2 subcommand1:
          option1: value
          option2: value

          # The options starting with x- or X- are ignored.
          x-internal-option: 1
          X-internal-option: 2
  """
  def _process(self, config, source):
    # Is it a dict?
    if not isinstance(config, dict):
      raise Exception(
          "YAML configuration from {0} needs to be a dictionary."
          .format(source)
      )

    # Does it have a list of commands?
    if "commands" not in config:
      raise Exception(
          "YAML configuration from {0} does not include commands."
          .format(source)
      )

    # Is commands a list?
    if not isinstance(config["commands"], list):
      raise Exception(
          "YAML configuration commands in {0} are not in a list."
          .format(source)
      )

    # Convert top-level dictionary into options.
    globals = [
        AWSCommand.get_option(name, value)
        for (name, value) in config.items()
        if name != "commands"
    ]

    # Process commands.
    commands = []
    for spec in config["commands"]:
      # Are commands dictionaries?
      if not isinstance(spec, dict):
        raise Exception(
            "Command '{0}' from file {1} is not a dictionary"
            .format(spec, source)
        )

      # Is there more than one command?
      if len(spec) > 1:
        raise Exception(
            "Command '{0}' from file {1} has too many instructions."
            .format(spec, source)
        )

      # Are the keys in the form 'command' or 'command subcommand'?
      (command_key, command_value) = spec.popitem()
      command = command_key.split()
      if len(command) > 2:
        raise Exception(
            "Command '{0}' from file {1} has too many parts."
            .format(spec, source)
        )

      # Are commands values dictionaries of options or None?
      if not (isinstance(command_value, dict) or command_value is None):
        raise Exception(
            "Command '{0}' from file {1} does not define options correctly."
            .format(spec, source)
        )

      # Convert to command.
      subcommand = command[1] if len(command) == 2 else None
      command = command[0]

      extentions = dict(
          (name[2:], config)
          for (name, config) in command_value.items()
          if name.startswith("x-") or name.startswith("X-")
      ) if command_value is not None else None
      options = [
          AWSCommand.get_option(name, value)
          for (name, value) in command_value.items()
          if not (name.startswith("x-") or name.startswith("X-"))
      ] if command_value is not None else None

      commands.append(AWSCommand(
        command, subcommand=subcommand,
        globals=globals, options=options,
        extentions=extentions
      ))

    return commands

  def load(self, path):
    with open(path, 'r') as data:
      config = yaml.load(data)
      return self._process(config, path)

  def loads(self, string):
    config = yaml.load(string)
    return self._process(config, "<string: {0}>".format(string))

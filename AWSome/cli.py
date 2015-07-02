import argparse
import sys

import yaml

from AWSome import __version__
from AWSome.executor import Executor
from AWSome.loader.factory import get_loader


class Client(object):
  """Interact with the command line and the user."""
  def _configure_parser(self):
    """
    Returns an instnace of the argument parser configured
    with the supported options.
    """
    parser = argparse.ArgumentParser(
        description="AWS command line client made awesome!",
        prog="AWSome"
    )

    # Options.
    parser.add_argument(
        "--execute", dest="execute", action="store_true", default=False,
        help="executes the generated command automatically."
    )
    parser.add_argument(
        "--profile", dest="profile", action="store", default=None,
        help="enables profile support and uses the specified profile file"
    )
    parser.add_argument(
        "--version", dest="action", action="store_const", const=self._version,
        default=None, help="prints version information and exit"
    )

    # Config files to process.
    parser.add_argument(
        "file", action="store", metavar="FILE", nargs="?",
        help="The YAML file to process"
    )

    return parser

  def _convert(self, options):
    """Load config file and convert it into a command."""
    if not options.file:
      raise Exception("I need a file to process.")

    loader = get_loader(options)
    commands = loader.load(options.file)

    for command in commands:
      cmd = command.format()
      if options.execute:
        print("[RUN>>>>>] " + cmd)
        executor = Executor(cmd)
        code = executor.run()
        if code != 0:
          print("[ERROR>>>] " + str(code))

      else:
        print(cmd)

    return 0

  def _version(self, options):
    """Print version information."""
    aws_ver_cmd = Executor("aws --version")
    aws_ver_cmd.run(buffer=True)
    aws_verison = aws_ver_cmd.stderr()

    print("--- Core ---")
    print("AWSome: " + __version__)

    print("--- Shells ---")
    print("AWS:    " + aws_verison)
    print("Python: " + sys.version)

    print("--- Libs ---")
    print("PyYaml: " + yaml.__version__)
    return 0

  def main(self, args):
    """Main enrty point for the tool."""
    parser = self._configure_parser()
    options = parser.parse_args(args)

    action = options.action or self._convert
    return action(options)

from abc import ABCMeta
from abc import abstractmethod


class Loader(object, metaclass=ABCMeta):
  """
  Abstract Loader class.

  Loaders are used to support differenct formats when it comes to
  loading the configurations to convert to aws commands.
  """
  def __init__(self, options):
    """Initialise the loader with the given options."""
    pass

  @abstractmethod
  def load(self, path):
    """Loads the requested file.
    :param str path: The path to the file to load.
    :returns: an instance of command.AWSCommand based on the loaded file.
    """
    pass

  @abstractmethod
  def loads(self, string):
    """Loads the configuration from a string.
    :param str string: The string to process.
    :returns: an instance of command.AWSCommand based on the loaded file.
    """
    pass

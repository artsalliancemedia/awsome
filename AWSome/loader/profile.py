import re

import yaml

from AWSome.loader import Loader


class ProfileLoader(Loader):
  """Pre-processes configuration files to inject profiles."""
  def __init__(self, options, loader):
    super(ProfileLoader, self).__init__(options)
    self._loader = loader
    self._profile = options.profile

  def load(self, path):
    with open(path) as config:
      return self.loads(config.read())

  def loads(self, string):
    with open(self._profile) as pro:
      profile = yaml.load(pro)

      def variable_expand(match):
        var_name = match.group(1).strip()
        node = profile
        parts = var_name.split('.')

        # Recursively lookup the variable in nested dicts.
        for part in parts:
          if part not in node:
            raise Exception(
                "Undefined variable {0} for profile {1}"
                .format(var_name, self._profile)
            )
          node = node[part]

        return node

      # Search and replace all variables.
      string = re.sub("\{\{(.*?)\}\}", variable_expand, string)
      return self._loader.loads(string)

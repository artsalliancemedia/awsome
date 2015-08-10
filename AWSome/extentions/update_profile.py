import json

import ruamel.yaml

from AWSome.extentions import Extention
from AWSome.extentions import SkipException


class UpdateProfile(Extention):
  """Updates a profile YAML with the result of a command."""
  def post_run(self, command, executor):
    # If the command failed do not bother.
    if executor.return_code() != 0:
      return

    # Check that all options are provided.
    if not self._options.profile:
      raise SkipExcetpion(
          "Updates to profile require a profile to update"
      )

    config = command.extentions.get("update-profile")
    if not config:
      # Nothing to do if the command does not update.
      return False

    if not config.get("key"):
      raise Excetpion(
          "Updates to profile require a key to update"
      )

    if not config.get("from"):
      raise Excetpion(
          "Updates to profile require a value to update from"
      )

    # Check that stdout is JSON decodable.
    data = None
    input = executor.stdout()
    try:
      data = json.loads(input)

    except ValueError:
      # Assume that the command failed because the configuration is
      # already applied to AWS and the profile is already up to date.
      raise SkipException("Profile update skipped as AWS output is not JSON")

    # Check that the JSON key is available.
    node = data
    sources = config["from"].split(".")
    for source in sources:
      if not isinstance(node, dict) or source not in node:
        raise SkipException(
            "Profile update failed as source '{0}' is missing".format(config["from"])
        )
      node = node[source]
    source_value = node

    # Load the profile.
    profile_file = open(self._options.profile)
    profile = ruamel.yaml.load(profile_file, ruamel.yaml.RoundTripLoader)
    profile_file.close()

    # Check that the profile key is available.
    node = profile
    sources = config["key"].split(".")
    for source in sources[:-1]:
      if not isinstance(node, dict):
        raise Exception(
            "Profile update failed as key '{0}' is missing in profile"
            .format(config["key"])
        )
      if source not in node:
        node[source] = {}
      node = node[source]

    # Ensure that the last node is valid too.
    source = sources[-1]
    if not isinstance(node, dict):
      raise Exception(
          "Profile update failed as key '{0}' is missing in profile"
          .format(config["key"])
      )

    # Update the profile.
    node[source] = source_value
    profile_file = open(self._options.profile, 'w')
    profile_file.write(ruamel.yaml.dump(
        profile, Dumper=ruamel.yaml.RoundTripDumper
    ))
    profile_file.close()
    return True

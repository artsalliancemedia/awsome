from AWSome.loader.profile import ProfileLoader
from AWSome.loader.yaml import YamlLoader


def get_loader(options):
  """Returns a loader based on the given options."""
  if options.profile:
    yaml = YamlLoader(options)
    return ProfileLoader(options, yaml)

  return YamlLoader(options)

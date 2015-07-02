from AWSome.loader.factory import get_loader
from AWSome.loader.profile import ProfileLoader
from AWSome.loader.yaml import YamlLoader

from tests.fixtures import options


def test_default_loader_is_yaml(options):
  loader = get_loader(options)
  assert isinstance(loader, YamlLoader)


def test_setting_profiles_enables_the_profile_loader(options):
  options.profile = "test.profile"
  loader = get_loader(options)
  assert isinstance(loader, ProfileLoader)


def test_profile_loader_uses_yaml_loader():
  options.profile = "test.profile"
  loader = get_loader(options)
  assert isinstance(loader._loader, YamlLoader)

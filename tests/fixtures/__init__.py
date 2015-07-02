import os
from tempfile import NamedTemporaryFile

import pytest


def stub_file(request, content):
  """
  Creates a temporary file and deletes it after the test is over.
  Returns the path to the file.
  """
  config = NamedTemporaryFile(delete=False, mode='w')
  config.write(content)
  config.close()

  def cleanup():
    os.unlink(config.name)
  request.addfinalizer(cleanup)

  return config.name


@pytest.fixture
def options():
  """Stub version of the parsed command line options."""
  class StubOptions(object):
    profile = None

  return StubOptions()

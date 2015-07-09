import sys

from AWSome.extentions import SkipException
from AWSome.extentions.update_profile import UpdateProfile


class ExtentionsManager(object):
  """Manages the execution of extentions."""
  # Maps all known extentions to a constructor.
  EXTENTIONS = {
      "update-profile": UpdateProfile
  }

  # Set of extentions that should run after the AWS command is executed.
  POST_RUN = set([
    "update-profile"
  ])

  def __init__(self, options):
    self._loaded_extentions = {}
    self._options = options

  def _get_extention(self, name):
    if name not in self._loaded_extentions:
      constructor = ExtentionsManager.EXTENTIONS[name]
      self._loaded_extentions[name] = constructor(self._options)
    return self._loaded_extentions[name]

  def post_run(self, command, executor):
    """Executes extentions after the AWS command finished executing."""
    # Make sure the command ouptut makes it to the user.
    sys.stderr.write(executor.stderr())
    sys.stdout.write(executor.stdout())

    # Look for configured exetentions.
    configured = set(command.extentions.keys())
    extentions = configured & ExtentionsManager.POST_RUN

    # Execute the extentions.
    reload_conf = False
    for extention in extentions:
      try:
        ext = self._get_extention(extention)
        reload_conf = ext.post_run(command, executor) or reload_conf

      except SkipException as ex:
        sys.stderr.write(
            "[ERROR] Profile update failed: {0}. Moving on.".format(str(ex))
        )

    return reload_conf

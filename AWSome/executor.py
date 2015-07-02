import sys
from subprocess import PIPE
from subprocess import Popen


class Executor(object):
  """Helper class to execute commands."""
  def __init__(self, command):
    self._command = command
    self._stderr = None
    self._stdout = None

  def run(self, buffer=False):
    process = Popen(
        self._command, shell=True,
        stderr=PIPE if buffer else None,
        stdout=PIPE if buffer else None
    )

    if buffer:
      (stdout, stderr) = process.communicate()
      self._stdout = stdout
      self._stderr = stderr

    else:
      process.wait()

    return process.returncode

  def stderr(self):
    if self._stderr:
      return self._stderr.decode('utf-8').strip()
    return ""

  def stdout(self):
    if self._stdout:
      return self._stdout.decode('utf-8').strip()
    return ""

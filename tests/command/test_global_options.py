from AWSome.command import AWSCommand


def test_command_is_added():
  command = AWSCommand("ec2")
  cmd = command.format()
  assert cmd == "aws ec2"


def test_command_option_is_added():
  options = [AWSCommand.get_option("a", "b")]
  command = AWSCommand("ec2", options=options)
  cmd = command.format()
  assert cmd == 'aws ec2 --a="b"'


def test_full_command():
  globals = [AWSCommand.get_option("debug", True)]
  options = [
      AWSCommand.get_option("description", "test-group"),
      AWSCommand.get_option("group-name", "test-group"),
      AWSCommand.get_option("vpc-id", "vpc-ca3285af")
  ]
  command = AWSCommand(
      "ec2", subcommand="create-security-group",
      globals=globals, options=options
  )
  cmd = command.format()
  assert cmd == (
    'aws --debug ec2 create-security-group --description="test-group" '
    '--group-name="test-group" --vpc-id="vpc-ca3285af"'
  )


def test_global_list_is_added():
  globals = [AWSCommand.get_option("a", ["b", "c", 'd\"e'])]
  command = AWSCommand("cmd", globals=globals)
  cmd = command.format()
  assert cmd == 'aws --a "b" "c" "d\\"e" cmd'


def test_global_string_is_added():
  globals = [AWSCommand.get_option("a", "b")]
  command = AWSCommand("cmd", globals=globals)
  cmd = command.format()
  assert cmd == 'aws --a="b" cmd'


def test_global_bool_is_false():
  globals = [AWSCommand.get_option("a", False)]
  command = AWSCommand("cmd", globals=globals)
  cmd = command.format()
  assert cmd == 'aws --no-a cmd'


def test_global_bool_is_true():
  globals = [AWSCommand.get_option("a", True)]
  command = AWSCommand("cmd", globals=globals)
  cmd = command.format()
  assert cmd == 'aws --a cmd'


def test_string_quotes_are_escaped():
  globals = [AWSCommand.get_option("a", 'b"c')]
  command = AWSCommand("cmd", globals=globals)
  cmd = command.format()
  assert cmd == 'aws --a="b\\"c" cmd'


def test_subcommand_is_added():
  command = AWSCommand("ec2", subcommand="create-security-group")
  cmd = command.format()
  assert cmd == "aws ec2 create-security-group"

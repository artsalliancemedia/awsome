import sys

from AWSome.cli import Client


if __name__ == "__main__":
  client = Client()
  exit_code = client.main(sys.argv[1:])
  sys.exit(exit_code)

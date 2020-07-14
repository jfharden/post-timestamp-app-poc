import subprocess


class BaseCommand:
    """Base command for other commands to inherit from giving common behaviour
    """
    def __init__(self, stdin, stdout, stderr):
        """Initialiser

        Args:
            stdin (file): file IO object to use for stdin.
            stdout (file): file IO object to use for stdout.
            stderr (file): file IO object to use for stderr.
        """
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def _run(self, command, cwd=None):
        """Execute the command given using stdin, stdout, and stderr provided in init.

        Args:
            command (list): List of command arguments to execute

        Keyword Args:
            cwd (string): If set the current working directory will be changed to this for execution

        Returns:
            Instance of subprocess.CompletedProcess
        """
        self.stdout.write("\nExecuting command: {}\n".format(" ".join(command)))
        self.stdout.write("="*119)
        self.stdout.write("\n")
        return subprocess.run(command, cwd=cwd, stdin=self.stdin, stdout=self.stdout, stderr=self.stderr)

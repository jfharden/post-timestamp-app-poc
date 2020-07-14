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

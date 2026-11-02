import game.commands.command as command_module


class CommandParser:
    def __init__(
        self,
        *,
        validVerbs: dict[str, str],
    ) -> None:
        self.validVerbs: dict[str, str] = validVerbs

    def parse(self, raw: str) -> command_module.Command:
        """Split a recognized verb and its optional argument into a command."""
        if not self.isValid(raw):
            raise ValueError("Enter a recognized command.")

        parts = raw.strip().split(maxsplit=1)
        verb = self.validVerbs[parts[0].lower()]
        arg = parts[1] if len(parts) > 1 else ""
        return command_module.Command(verb=verb, arg=arg)

    def isValid(self, raw: str) -> bool:
        """Return whether the input starts with a configured command verb."""
        parts = raw.split(maxsplit=1)
        return bool(parts) and parts[0].lower() in self.validVerbs

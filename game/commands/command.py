class Command:
    def __init__(
        self,
        *,
        verb: str,
        arg: str,
    ) -> None:
        self.verb: str = verb
        self.arg: str = arg

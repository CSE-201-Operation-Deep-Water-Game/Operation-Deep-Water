"""Command scaffolding from the class diagram."""

from __future__ import annotations


class Command:
    """Scaffold for Command from the class diagram."""

    def __init__(
        self,
        *,
        verb: str,
        arg: str,
    ) -> None:
        self.verb: str = verb
        self.arg: str = arg

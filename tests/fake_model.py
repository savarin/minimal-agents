from agents.models.interface import Model
from agents.items import (
    TResponseOutputItem,
)


class FakeModel(Model):
    def __init__(
        self,
        initial_output: list[TResponseOutputItem] | Exception | None = None,
    ) -> None:
        if initial_output is None:
            initial_output = []

        self.turn_outputs: list[list[TResponseOutputItem] | Exception] = (
            [initial_output] if initial_output else []
        )

    def set_next_output(self, output: list[TResponseOutputItem] | Exception) -> None:
        self.turn_outputs.append(output)

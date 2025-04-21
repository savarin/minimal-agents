from agents import (
    Model,
    ModelResponse,
    ModelSettings,
    TResponseInputItem,
    TResponseOutputItem,
    Usage,
)


class FakeModel(Model):
    def __init__(
        self,
        initial_output: list[TResponseOutputItem] | None = None,
    ) -> None:
        if initial_output is None:
            initial_output = []

        self.turn_outputs: list[list[TResponseOutputItem]] = (
            [initial_output] if initial_output else []
        )

    def get_next_output(self) -> list[TResponseOutputItem]:
        if not self.turn_outputs:
            return []

        return self.turn_outputs.pop(0)

    async def get_response(
        self,
        system_instructions: str | None,
        input: str | list[TResponseInputItem],
        model_settings: ModelSettings,
    ) -> ModelResponse:
        self.last_turn_args = {
            "system_instructions": system_instructions,
            "input": input,
            "model_settings": model_settings,
        }

        output = self.get_next_output()

        return ModelResponse(
            output=output,
            usage=Usage(),
            response_id=None,
        )

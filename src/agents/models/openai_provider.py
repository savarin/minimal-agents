import os

from openai import AsyncOpenAI
from openai.types import ChatModel
from openai.types.responses import ResponseOutputMessage, ResponseOutputText

from .interface import (
    Model,
    ModelProvider,
    ModelResponse,
    ModelSettings,
    Usage,
    TResponseInputItem,
)


# from .openai_chatcompletions import OpenAIChatCompletionsModel


FAKE_RESPONSES_ID = "__fake_id__"


class OpenAIChatCompletionsModel(Model):
    def __init__(
        self,
        model: str | ChatModel,
        openai_client: AsyncOpenAI,
    ) -> None:
        self.model = model
        self._client = openai_client

    async def get_response(
        self,
        system_instructions: str | None,
        input: str | list[TResponseInputItem],
        model_settings: ModelSettings,
    ) -> ModelResponse:
        messages = [
            {
                "content": system_instructions,
                "role": "system",
            },
            {
                "content": input,
                "role": "user",
            },
        ]

        response = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore[arg-type]
        )

        items = [
            ResponseOutputMessage(
                id=FAKE_RESPONSES_ID,
                content=[
                    ResponseOutputText(
                        text=response.choices[0].message.content,  # type: ignore[arg-type]
                        type="output_text",
                        annotations=[],
                    )
                ],
                role="assistant",
                type="message",
                status="completed",
            )
        ]

        usage = (
            Usage(
                requests=1,
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )
            if response.usage
            else Usage()
        )

        return ModelResponse(
            output=items,  # type: ignore
            usage=usage,
            response_id=None,
        )


# src.agents.models.openai_provider


DEFAULT_MODEL: str = "gpt-4o"


class OpenAIProvider(ModelProvider):
    def __init__(
        self,
        api_key: str | None = None,
    ) -> None:
        """Create a new OpenAI provider.

        Args:
            api_key: The API key to use for the OpenAI client. If not provided, we will use the
                default API key.
        """

    # We lazy load the client in case you never actually use OpenAIProvider(). Otherwise
    # AsyncOpenAI() raises an error if you don't have an API key set.
    def _get_client(self) -> AsyncOpenAI:
        return AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    def get_model(self, model_name: str | None) -> Model:
        if model_name is None:
            model_name = DEFAULT_MODEL

        client = self._get_client()

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

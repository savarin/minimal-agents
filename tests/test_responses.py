from openai.types.responses import (
    ResponseOutputItem,
    ResponseOutputMessage,
    ResponseOutputText,
)


def get_text_message(content: str) -> ResponseOutputItem:
    return ResponseOutputMessage(
        id="1",
        type="message",
        role="assistant",
        content=[ResponseOutputText(text=content, type="output_text", annotations=[])],
        status="completed",
    )

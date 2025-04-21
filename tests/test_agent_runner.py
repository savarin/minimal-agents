from typing import Any
import pytest

from openai.types.responses import (
    ResponseOutputItem,
    ResponseOutputMessage,
    ResponseOutputText,
)

from agents import Agent, Runner, TResponseInputItem

from .fake_model import FakeModel


# from .test_responses import get_text_message


def get_text_input_item(content: str) -> TResponseInputItem:
    return {
        "content": content,
        "role": "user",
    }


def get_text_message(content: str) -> ResponseOutputItem:
    return ResponseOutputMessage(
        id="1",
        type="message",
        role="assistant",
        content=[ResponseOutputText(text=content, type="output_text", annotations=[])],
        status="completed",
    )


# tests.test_agent_runner


@pytest.mark.asyncio
async def test_simple_first_run() -> None:
    model = FakeModel()
    agent = Agent[Any](
        name="test",
        model=model,
    )
    model.set_next_output([get_text_message("first")])

    result = await Runner.run(agent, input="test")
    assert result.input == "test"
    assert len(result.new_items) == 1, "exactly one item should be generated"
    assert result.final_output == "first"
    assert len(result.raw_responses) == 1, (
        "exactly one model response should be generated"
    )
    assert result.raw_responses[0].output == [get_text_message("first")]
    assert result.last_agent == agent

    assert len(result.to_input_list()) == 2, (
        "should have original input and generated item"
    )

    model.set_next_output([get_text_message("second")])

    result = await Runner.run(
        agent,
        input=[get_text_input_item("message"), get_text_input_item("another_message")],
    )
    assert len(result.new_items) == 1, "exactly one item should be generated"
    assert result.final_output == "second"
    assert len(result.raw_responses) == 1, (
        "exactly one model response should be generated"
    )
    assert len(result.to_input_list()) == 3, (
        "should have original input and generated item"
    )

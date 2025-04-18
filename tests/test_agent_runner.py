import pytest

from agents import Agent

from .fake_model import FakeModel
from .test_responses import get_text_message


@pytest.mark.asyncio
async def test_simple_first_run() -> None:
    model = FakeModel()
    Agent(
        name="test",
        model=model,
    )
    model.set_next_output([get_text_message("first")])

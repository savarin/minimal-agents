import pytest

from agents import Agent

from .fake_model import FakeModel


@pytest.mark.asyncio
async def test_simple_first_run() -> None:
    model = FakeModel()
    Agent(
        name="test",
        model=model,
    )

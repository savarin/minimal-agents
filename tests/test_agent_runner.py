import pytest

from .fake_model import FakeModel


@pytest.mark.asyncio
async def test_simple_first_run() -> None:
    FakeModel()

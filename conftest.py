"""Root pytest config.

- Defaults to DENYING live Anthropic API calls — strip ANTHROPIC_API_KEY from
  the environment unless `RUN_LIVE_LLM=1` is explicitly set.
- Registers the `@pytest.mark.live` marker so test files can gate live smokes.
- Phase 1b will wire pytest-vcr cassette autoload here.
"""

from __future__ import annotations

import os

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "live: tests that hit the real Anthropic API; require RUN_LIVE_LLM=1",
    )


@pytest.fixture(autouse=True)
def _block_live_llm(monkeypatch: pytest.MonkeyPatch) -> None:
    """Strip ANTHROPIC_API_KEY unless RUN_LIVE_LLM=1 is set explicitly."""
    if os.getenv("RUN_LIVE_LLM") != "1":
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if os.getenv("RUN_LIVE_LLM") == "1":
        return
    skip_live = pytest.mark.skip(reason="live tests require RUN_LIVE_LLM=1")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)

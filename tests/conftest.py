import pytest


@pytest.fixture
def crates():
    return {
        "minimal": "./tests/crates/minimal",
        "wide": "./tests/crates/wide",
        "textfiles": "./tests/crates/textfiles",
    }

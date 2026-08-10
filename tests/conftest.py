from pathlib import Path

import pytest

from lipikar.config import AppConfig, load_config

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def config_dir() -> Path:
    return REPO_ROOT / "configs"


@pytest.fixture(scope="session")
def config(config_dir: Path) -> AppConfig:
    return load_config(AppConfig, config_dir, environ={})

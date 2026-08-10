import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GUARD_SCRIPT = REPO_ROOT / "scripts" / "check_no_sensitive_files.py"
GUARD_MODULE = "privacy_guard"


@pytest.fixture(scope="session")
def guard() -> ModuleType:
    """Loaded by path because the guard is deliberately not part of the installable package."""
    spec = importlib.util.spec_from_file_location(GUARD_MODULE, GUARD_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[GUARD_MODULE] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "path",
    [
        "data/raw/page_0142.jpg",
        "data/processed/page_0142.json",
        "data/lexicon/terms.txt",
    ],
)
def test_anything_under_data_is_rejected(guard: ModuleType, path: str) -> None:
    violations = guard.find_violations([path], guard.load_config())
    assert [violation.path for violation in violations] == [path]


def test_windows_separators_do_not_bypass_the_guard(guard: ModuleType) -> None:
    violations = guard.find_violations(["data\\raw\\page_0142.jpg"], guard.load_config())
    assert len(violations) == 1


@pytest.mark.parametrize("path", ["page_0142.png", "scans/deed.pdf", "docs/deed.tiff"])
def test_images_outside_the_allowed_prefix_are_rejected(guard: ModuleType, path: str) -> None:
    assert guard.find_violations([path], guard.load_config())


@pytest.mark.parametrize("path", ["checkpoints/best.pt", "export/model.onnx", "m.safetensors"])
def test_model_weights_are_rejected(guard: ModuleType, path: str) -> None:
    assert guard.find_violations([path], guard.load_config())


@pytest.mark.parametrize(
    "path",
    [
        "docs/assets/redacted_sample.png",
        "lipikar/shuddhi/metrics.py",
        "configs/default.yaml",
        "data/raw/.gitkeep",
    ],
)
def test_legitimate_paths_are_allowed(guard: ModuleType, path: str) -> None:
    assert guard.find_violations([path], guard.load_config()) == []


def test_guard_fails_closed_when_its_config_is_missing(guard: ModuleType, tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        guard.load_config(tmp_path / "absent.json")


def test_tracked_tree_is_clean(guard: ModuleType) -> None:
    tracked = guard.collect_paths([], True)[0]
    assert guard.find_violations(tracked, guard.load_config()) == []

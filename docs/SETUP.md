# Lipikar — Setup guide

How to get a working development environment. Written for Windows (the primary development machine)
with notes for macOS and Linux.

> **Current state:** the Python packaging files (`pyproject.toml`, `requirements-dev.txt`) are
> delivered by **story 1.1**, which has not been implemented yet. Until it lands, steps 3–5 below
> will not work. Step 6 (the privacy guard) works today because it is stdlib-only.

---

## 1. Prerequisites

| Requirement | Version | Why |
|---|---|---|
| Python | **3.11 or 3.12** | Not 3.14 — see the warning below |
| Git | any recent | — |
| A code editor | VS Code recommended | — |
| NVIDIA GPU | optional | Not required for development; training uses rented GPUs |

### ⚠️ Do not use Python 3.14

The system Python on the development machine is **3.14.5**, which is ahead of PyTorch's wheel
availability. Installing the ML stack on it will either fail or attempt a source build. This is
recorded as **ADR-001** in [`architecture.md`](architecture.md).

Check what you have:

```bash
python --version
```

If it reports 3.14, install 3.12 alongside it — you do not need to remove 3.14.

**Windows:** download the 3.12 installer from python.org, or use `winget`:

```powershell
winget install Python.Python.3.12
```

Then verify the versioned launcher can see it:

```powershell
py -3.12 --version
```

**macOS / Linux:** use `pyenv`:

```bash
pyenv install 3.12.8
pyenv local 3.12.8
```

---

## 2. Clone

```bash
git clone https://github.com/saidul-islam-rajib/Lipikar.git
cd Lipikar
```

---

## 3. Create the virtual environment

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Windows (Git Bash):**

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
```

**macOS / Linux:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Confirm you are in the venv and on the right Python:

```bash
python --version      # expect 3.12.x
```

---

## 4. Install dependencies

*(Available after story 1.1.)*

```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

`-e .` installs Lipikar in editable mode, so `import lipikar` resolves to your working tree.

---

## 5. Verify

*(Available after story 1.1.)*

```bash
pytest -q                 # full suite — must be green (R50.0)
ruff check .              # lint
ruff format --check .     # formatting
mypy lipikar              # type check
```

All four must pass before you claim any work is done. That is not a convention here, it is
[Rule 50.0](../.bmad/rules/50-definition-of-done.md).

---

## 6. Verify the privacy guard

This works right now, with no dependencies installed:

```bash
python scripts/check_no_sensitive_files.py --all
```

Expected: `privacy guard: OK`.

Confirm it actually blocks things:

```bash
python scripts/check_no_sensitive_files.py data/raw/example.jpg
```

Expected: exit code 1 with an explanation. If this passes instead of failing, **stop and fix it** —
it is the only automated defence against committing real deed images, and git history is permanent.

### Install it as a pre-commit hook (recommended)

```bash
printf '#!/bin/sh\npython scripts/check_no_sensitive_files.py\n' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Now every `git commit` checks staged files first. Note `.git/hooks/` is not version-controlled, so
each clone needs this done once.

---

## 7. Configure git identity

The repository ships a local identity so commits attribute correctly (see
[Rule 60](../.bmad/rules/60-git-and-commits.md)). Verify it:

```bash
git config --local --get user.email
```

Expected: `96372056+saidul-islam-rajib@users.noreply.github.com`.

If you are a different contributor, set your own **repo-locally** — never rely on a global work
email here.

---

## 8. Data directories

`data/` exists with empty subdirectories and is **gitignored**:

```
data/raw/          original deed photographs
data/interim/      restored pages, line crops
data/processed/    training-ready datasets and manifests
data/lexicon/      revenue vocabulary for shuddhi
```

**Nothing under `data/` may ever be committed.** Deed images contain living people's names,
signatures, and biometric thumb impressions. Read
[Rule 30](../.bmad/rules/30-data-privacy.md) before you put a real document in there, and record its
provenance in [`DATA.md`](DATA.md) — data with no provenance entry may not be used.

---

## 9. Training on a rented GPU

There is no local NVIDIA GPU, so training stories run on rented hardware (Runpod, Vast.ai, Lambda).
A LoRA fine-tune of a 3–7B vision-language model wants roughly **24 GB VRAM**.

Every training story ships a launch script under `scripts/` recording the exact image, driver, and
CUDA versions used. Data does not travel with the code — the corpus is pulled from a private
location and the transfer method is recorded in [`DATA.md`](DATA.md).

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `torch` install fails or builds from source | Python 3.14 | Use 3.11/3.12 (ADR-001) |
| `Activate.ps1 cannot be loaded` | PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `ModuleNotFoundError: lipikar` | Editable install missing | `pip install -e .` with the venv active |
| Bengali text renders as boxes in the terminal | Font lacks Bengali glyphs | Use a font with Bengali coverage; does not affect correctness |
| Bengali text garbled in a file | Encoding, not content | Files are UTF-8 without BOM (R00.8) — fix the encoding path, never transliterate |
| Guard fails with a config error | `configs/privacy_guard.json` missing | Intentional fail-closed (ADR-004); restore the file |
| Commit rejected by pre-commit hook | Staged file violates Rule 30 | Unstage it. Do not use `--no-verify` (R60.6) |

---

## Next

Read [`USER_GUIDE.md`](USER_GUIDE.md) for how work actually flows through this repository.

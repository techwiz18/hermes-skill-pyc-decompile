# pyc-decompile (Hermes skill)

Inspect compiled Python bytecode (`.pyc`) when no `.py` sources exist — built for modding SDKs like The Sims 4's Lot51 core-library (Python 3.7 bytecode), useful for any `.pyc`-only dependency.

Two tiers:
1. **API listing** — `scripts/pyc_list.py` bootstraps its own venv with `xdis` (cross-version reader) and prints every class/function with signatures. Run it on a file or a directory.
2. **Full source recovery** — `pycdc` (build from https://github.com/zrax/pycdc). Best on Python ≤3.9 bytecode.

## Install
Copy this repo to `~/.hermes/skills/software-development/pyc-decompile/` (or install via `hermes skills install`), then use it from any session: "load the `pyc-decompile` skill".

## Rule it enforces
Never invent API methods for a bytecode-only library — recover signatures first, report unknowns explicitly.

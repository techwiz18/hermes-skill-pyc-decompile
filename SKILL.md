---
name: pyc-decompile
description: Inspect compiled Python bytecode (.pyc) when no .py sources exist — list classes/functions/signatures via xdis, full-source recovery via pycdc. Use for modding SDKs, vendored bytecode, or any .pyc-only dependency.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [python, bytecode, decompile, reverse-engineering, modding, api-discovery]
    related_skills: [codebase-inspection, systematic-debugging]
---

# Python Bytecode (.pyc) Inspection

`.pyc` files contain no readable source, so `read_file`/`search_files` on them is useless for API discovery. This skill recovers the information in two tiers.

## Tier 1 — API listing (fast, always works)

`scripts/pyc_list.py` bootstraps its own venv with `xdis` (cross-version bytecode reader — required because e.g. Python 3.7 mod bytecode cannot be unmarshalled by newer interpreters) and prints every class, function, and method with signatures:

```bash
python3 ~/.hermes/skills/software-development/pyc-decompile/scripts/pyc_list.py <file.pyc>
python3 ~/.hermes/skills/software-development/pyc-decompile/scripts/pyc_list.py <directory>  # walks *.pyc recursively
```

Output is `qualified.name(arg1, arg2, ...)` one per line plus source-file/line hints. Use this FIRST to map an unknown bytecode library's API surface.

## Tier 2 — Full source recovery

`pycdc` decompiles to readable source. Expected at `~/.local/bin/pycdc` (built from https://github.com/zrax/pycdc); if missing, build it:

```bash
git clone https://github.com/zrax/pycdc.git /tmp/pycdc && cd /tmp/pycdc
cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j"$(nproc)"
cp build/pycdc ~/.local/bin/ && rm -rf /tmp/pycdc
```

Then: `pycdc <file.pyc>`. Best results on Python ≤3.9 bytecode (e.g. The Sims 4 ships 3.7). Newer-version output may be partial — fall back to Tier 1 for names/signatures.

## Rules

- NEVER invent API methods for a bytecode-only library. If neither tier yields a signature, report exactly which names are unknown instead of guessing.
- Prefer Tier 1 for broad mapping (cheap), Tier 2 for the 2–3 files that matter (slow but complete).

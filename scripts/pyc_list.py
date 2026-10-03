#!/usr/bin/env python3
"""List classes/functions/signatures from .pyc files of ANY Python version.

Bootstraps a venv with xdis on first run (system interpreters cannot
unmarshal bytecode from other versions, e.g. 3.7 mod files on 3.12).
Usage: pyc_list.py <file.pyc | directory> [--full]
  --full also prints first-line-number and constants preview per object.
"""
import os, subprocess, sys, venv

HERE = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(HERE, ".venv")
VPY = os.path.join(VENV, "bin", "python")


def ensure_env():
    if not os.path.exists(VPY):
        venv.create(VENV, with_pip=True)
        subprocess.check_call([VPY, "-m", "pip", "install", "-q", "xdis"])
    # Re-exec inside the venv so xdis is importable.
    if sys.executable != VPY:
        os.execv(VPY, [VPY, os.path.abspath(__file__)] + sys.argv[1:])


DUMP = r'''
import sys, os
from xdis import load_module

def walk(code, qual, depth=0, full=False):
    kind = "class" if code.co_name and code.co_firstlineno and _is_class(code) else "def"
    args = list(code.co_varnames[: code.co_argcount])
    if code.co_kwonlyargcount:
        args += ["*", *list(code.co_varnames[code.co_argcount: code.co_argcount + code.co_kwonlyargcount])]
    if code.co_flags & 0x04: args.append("*args")
    if code.co_flags & 0x08: args.append("**kwargs")
    print(f"{'  ' * depth}{kind} {qual}({', '.join(args)})  # line {code.co_firstlineno}")
    for const in code.co_consts:
        if hasattr(const, "co_name"):
            walk(const, f"{qual}.{const.co_name}" if qual != "<module>" else const.co_name, depth + 1, full)

def _is_class(code):
    # Heuristic: class bodies reference __module__ / __qualname__ in names.
    return "__module__" in code.co_names

path = sys.argv[1]
full = "--full" in sys.argv
targets = []
if os.path.isdir(path):
    for root, _, files in os.walk(path):
        targets += [os.path.join(root, f) for f in sorted(files) if f.endswith((".pyc", ".py"))]
else:
    targets = [path]
for t in targets:
    print(f"### {t}")
    try:
        code = load_module(t)[3]
        walk(code, "<module>", 0, full)
    except Exception as e:
        print(f"  !! could not parse: {e}")
'''

if __name__ == "__main__":
    ensure_env()
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(DUMP)
        inner = f.name
    os.execv(sys.executable, [sys.executable, inner] + sys.argv[1:])

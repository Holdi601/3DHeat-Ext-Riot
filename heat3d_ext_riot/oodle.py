"""
Oodle decompression, through a library you name.

The game's archives are compressed with Oodle (RAD Game Tools / Epic Games).
Oodle has no redistributable build, so this package carries none, downloads
none and looks for none: you pass the path of an `oo2core_9_win64.dll` from
software you have installed (`--oodle`, or `HEAT3D_OODLE` once). It is loaded
where it is, used on your machine only, and never copied.
"""

from __future__ import annotations

import ctypes
import os
from pathlib import Path

_lib: ctypes.CDLL | None = None
_path: Path | None = None

MISSING = (
    "This tool needs Oodle to read the game's archives, and does not include it.\n"
    "Pass the path of an oo2core_9_win64.dll from software you have installed: --oodle <path>\n"
    "(or set HEAT3D_OODLE to it). It is used where it is and never copied."
)


class OodleUnavailable(RuntimeError):
    pass


def _machine(path: Path) -> int | None:
    """The PE machine field of a DLL: 0x8664 is x64, which is what this Python can load."""
    try:
        with open(path, "rb") as f:
            head = f.read(4096)
        pe = int.from_bytes(head[0x3C:0x40], "little")
        return int.from_bytes(head[pe + 4 : pe + 6], "little")
    except (OSError, ValueError):
        return None


def load(given: str | os.PathLike[str] | None = None) -> ctypes.CDLL:
    """Load the library named by `given` or `HEAT3D_OODLE` once and keep it."""
    global _lib, _path
    if _lib is not None:
        return _lib
    chosen = given or os.environ.get("HEAT3D_OODLE")
    if not chosen:
        raise OodleUnavailable(MISSING)
    p = Path(chosen)
    if p.is_dir():
        p = p / "oo2core_9_win64.dll"
    if not p.is_file():
        raise OodleUnavailable(f"{p} does not exist.\n{MISSING}")
    if _machine(p) != 0x8664:
        raise OodleUnavailable(f"{p} is not a 64-bit x86 (x64) library, which this Python needs.\n{MISSING}")
    try:
        lib = ctypes.CDLL(str(p))
        fn = lib.OodleLZ_Decompress
    except (OSError, AttributeError) as e:
        raise OodleUnavailable(f"{p} could not be loaded as Oodle ({e}).\n{MISSING}") from e
    fn.restype = ctypes.c_ssize_t
    fn.argtypes = [ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_void_p, ctypes.c_ssize_t,
                   ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_ssize_t,
                   ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_int]
    _lib, _path = lib, p
    return lib


def path() -> Path | None:
    return _path


def decompress(src: bytes, size: int) -> bytes:
    lib = load()
    dst = ctypes.create_string_buffer(size)
    got = lib.OodleLZ_Decompress(src, len(src), dst, size, 1, 0, 0, None, 0, None, None, None, 0, 3)
    if got != size:
        raise ValueError(f"Oodle gave {got} bytes for {size}")
    return dst.raw

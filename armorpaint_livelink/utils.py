from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence


def search_textures(
    path: Path | str, textures: Sequence[Optional[str]]
) -> List[Optional[str]]:
    """Search ``path`` for common PBR texture files.

    The ``textures`` sequence should contain seven items corresponding to
    ``base``, ``metal``, ``normal``, ``rough``, ``ao``, ``height`` and
    ``emissive`` textures. If a matching texture is found in ``path`` the
    resulting list entry is replaced with the full string path to that file.
    """
    path = Path(path)
    result: List[Optional[str]] = list(textures)

    suffix_map = {
        "_base": 0,
        "_metal": 1,
        "_normal": 2,
        "_rough": 3,
        "_ao": 4,
        "_height": 5,
        "_emit": 6,
    }

    for file in path.iterdir():
        if not file.is_file():
            continue
        for suffix, idx in suffix_map.items():
            if file.stem.endswith(suffix):
                result[idx] = str(file)
                break

    return result

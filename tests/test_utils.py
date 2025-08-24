from pathlib import Path
import importlib.util
import sys, types

sys.modules.setdefault("bpy", types.SimpleNamespace())

spec = importlib.util.spec_from_file_location(
    "armorpaint_utils", Path(__file__).resolve().parents[1] / "armorpaint_livelink" / "utils.py"
)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)
search_textures = utils.search_textures


def test_search_textures(tmp_path: Path):
    (tmp_path / "mat_base.png").write_text("base")
    (tmp_path / "mat_rough.jpg").write_text("rough")
    textures = [None] * 7
    result = search_textures(tmp_path, textures)
    assert result[0].endswith("mat_base.png")
    assert result[3].endswith("mat_rough.jpg")

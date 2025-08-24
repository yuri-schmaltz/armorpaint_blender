import os

import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, BoolProperty

from .utils import SEP


def update_filename(self, context):
    """Ensure filename ends with .arm and exists."""
    if not self["filename"].endswith(".arm") and self["filename"] != "":
        self["filename"] += ".arm"

    obj = bpy.data.objects[context.active_object.name]
    if "armorpaint_filename" in obj:
        path = obj["armorpaint_proj_dir"] + SEP + self["filename"]
        if os.path.isfile(path):
            obj["armorpaint_filename"] = self["filename"]
        else:
            self["filename"] = "ERROR: File not found"


class ArmorPaintLiveLinkProperties(PropertyGroup):
    """Scene properties used by the ArmorPaint add-on."""

    project_path = StringProperty(
        name="ArmorPaint Project Directory",
        description="Path to ArmorPaint Project Directory",
        default="//",
        maxlen=1024,
        subtype="DIR_PATH",
    )

    use_custom_filename = BoolProperty(
        name="Use custom filename",
        description="",
        default=False,
    )

    filename = StringProperty(
        name="ArmorPaint File name",
        description="File name",
        default="",
        update=update_filename,
    )

    use_custom_texture_dir = BoolProperty(
        name="Use custom texture dir",
        description="",
        default=False,
    )

    texture_path = StringProperty(
        name="ArmorPaint Texture Directory",
        description="Texture directory",
        default=SEP + "exports" + SEP,
        maxlen=1024,
        subtype="DIR_PATH",
    )

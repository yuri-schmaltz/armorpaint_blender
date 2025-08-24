from __future__ import annotations

from pathlib import Path

import bpy
from bpy.props import BoolProperty, PointerProperty, StringProperty
from bpy.types import AddonPreferences, PropertyGroup


def update_filename(self, context):
    """Ensure the project filename ends with ``.arm``."""
    filename = self["filename"]
    if filename and not filename.endswith(".arm"):
        filename += ".arm"
        self["filename"] = filename

    obj = bpy.data.objects[context.active_object.name]
    proj_dir = Path(obj.get("armorpaint_proj_dir", ""))
    if proj_dir and (proj_dir / filename).is_file():
        obj["armorpaint_filename"] = filename
    else:
        self["filename"] = "ERROR: File not found"


class ArmorPaintLiveLinkProperties(PropertyGroup):
    project_path: StringProperty = StringProperty(
        name="ArmorPaint Project Directory",
        description="Path to ArmorPaint Project Directory",
        default="//",
        maxlen=1024,
        subtype="DIR_PATH",
    )

    use_custom_filename: BoolProperty = BoolProperty(
        name="Use custom filename",
        description="",
        default=False,
    )

    filename: StringProperty = StringProperty(
        name="ArmorPaint File name",
        description="File name",
        default="",
        update=update_filename,
    )

    use_custom_texture_dir: BoolProperty = BoolProperty(
        name="Use custom texture dir",
        description="",
        default=False,
    )

    texture_path: StringProperty = StringProperty(
        name="ArmorPaint Texture Directory",
        description="Texture directory",
        default=Path("exports").as_posix(),
        maxlen=1024,
        subtype="DIR_PATH",
    )


class ArmorPaintLiveLinkAddonPreferences(AddonPreferences):
    bl_idname = __name__

    path_exe: StringProperty = StringProperty(
        name="ArmorPaint Executable",
        subtype="FILE_PATH",
    )

    def draw(self, context):
        layout = self.layout
        system = bpy.app.build_platform
        if system.startswith("Windows"):
            layout.label(text="Please select the location of the ArmorPaint.exe")
        elif system.startswith("Linux"):
            layout.label(
                text=(
                    "Please select this path: "
                    "'ArmorPaint-Installation-Path/ArmorPaint'"
                )
            )
        elif system.startswith("Darwin"):
            layout.label(
                text=(
                    "Please select this path: "
                    "'ArmorPaint-Installation-Path/ArmorPaint.app/Contents/MacOS/'"
                )
            )
        layout.prop(self, "path_exe")


def register_properties():
    bpy.types.Scene.armorpaint_properties = PointerProperty(
        type=ArmorPaintLiveLinkProperties
    )


def unregister_properties():
    del bpy.types.Scene.armorpaint_properties

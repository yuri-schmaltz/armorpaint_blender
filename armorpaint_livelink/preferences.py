from bpy.types import AddonPreferences
from bpy.props import StringProperty

from .utils import SYSTEM


class ArmorPaintLiveLinkAddonPreferences(AddonPreferences):
    """Store add-on preferences such as the ArmorPaint executable path."""

    bl_idname = __package__

    path_exe = StringProperty(name="ArmorPaint Executable", subtype="FILE_PATH")

    def draw(self, _context):
        layout = self.layout
        if SYSTEM == "Windows":
            layout.label(text="Please select the location of the ArmorPaint.exe")
        elif SYSTEM == "Linux":
            layout.label(
                text=(
                    "Please select this path: "
                    '"ArmorPaint-Installation-Path/ArmorPaint"'
                )
            )
        elif SYSTEM == "Darwin":
            layout.label(
                text=(
                    "Please select this path: "
                    '"ArmorPaint-Installation-Path/ArmorPaint.app/Contents/MacOS/"'
                )
            )
        layout.prop(self, "path_exe")

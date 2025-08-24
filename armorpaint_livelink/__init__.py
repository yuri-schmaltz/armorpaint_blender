# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty

from .properties import ArmorPaintLiveLinkProperties
from .preferences import ArmorPaintLiveLinkAddonPreferences
from .operators import (
    ArmorPaintLiveLinkOperator,
    ArmorPaintLiveLinkTexturesLoaderOperator,
)
from .ui import (
    ArmorPaintProjectFolder,
    ArmorPaintOpenPanel,
    ArmorPaintSyncTexturesPanel,
)

bl_info = {
    "name": "ArmorPaint Live-Link",
    "author": "PiloeGAO (Leo DEPOIX), Spirou4D, luboslenco",
    "version": (0, 9, 0),
    "blender": (3, 6, 0),
    "location": "3D View > Side Bar",
    "description": "Integration of ArmorPaint into Blender",
    "warning": "Development",
    "wiki_url": "https://github.com/armory3d/armorpaint_blender",
    "tracker_url": "https://github.com/armory3d/armorpaint_blender/issues",
    "category": "Paint",
}

classes = (
    ArmorPaintLiveLinkProperties,
    ArmorPaintLiveLinkAddonPreferences,
    ArmorPaintLiveLinkOperator,
    ArmorPaintLiveLinkTexturesLoaderOperator,
    ArmorPaintProjectFolder,
    ArmorPaintOpenPanel,
    ArmorPaintSyncTexturesPanel,
)


def register():
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.armorpaint_properties = PointerProperty(
        type=ArmorPaintLiveLinkProperties
    )


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.armorpaint_properties


if __name__ == "__main__":
    register()

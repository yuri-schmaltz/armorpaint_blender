from __future__ import annotations

from bpy.utils import register_class, unregister_class

from .operators import (
    ArmorPaintLivelinkOperator,
    ArmorPaintLivelinkTexturesLoaderOperator,
)
from .properties import (
    ArmorPaintLiveLinkAddonPreferences,
    ArmorPaintLiveLinkProperties,
    register_properties,
    unregister_properties,
)
from .ui import (
    ArmorPaintOpenPanel,
    ArmorPaintProjectFolder,
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
    ArmorPaintLivelinkOperator,
    ArmorPaintLivelinkTexturesLoaderOperator,
    ArmorPaintProjectFolder,
    ArmorPaintOpenPanel,
    ArmorPaintSyncTexturesPanel,
)


def register():
    for cls in classes:
        register_class(cls)
    register_properties()


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    unregister_properties()


if __name__ == "__main__":
    register()

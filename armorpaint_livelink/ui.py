"""User interface panels for ArmorPaint live link."""

from __future__ import annotations

from pathlib import Path

import bpy
from bpy.types import Panel


class View3DPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ArmorPaint"

    @classmethod
    def poll(cls, context):
        return context.object is not None


class ArmorPaintProjectFolder(View3DPanel, Panel):
    bl_idname = "VIEW3D_PT_armorpaint"
    bl_label = "ArmorPaint Live-link"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Project Directory :")
        col.prop(scene.armorpaint_properties, "project_path", text="")


class ArmorPaintOpenPanel(View3DPanel, Panel):
    bl_idname = "VIEW3D_PT_armorpaint_open_panel"
    bl_label = "Open ArmorPaint"

    def draw(self, context):
        scene = context.scene
        obj = context.active_object
        use_custom = scene.armorpaint_properties.use_custom_filename
        layout = self.layout
        col = layout.split().column()

        if obj.type == "MESH":
            col.prop(
                scene.armorpaint_properties,
                "use_custom_filename",
                text="Custom File Name",
            )
            if use_custom:
                col.prop(scene.armorpaint_properties, "filename", text="")
            col.operator(
                "object.armorpaint_livelink",
                text="Open in ArmorPaint",
                icon="TPAINT_HLT",
            )
        else:
            col.label(icon="CANCEL", text="Only meshes can be exported")


class ArmorPaintSyncTexturesPanel(View3DPanel, Panel):
    bl_idname = "VIEW3D_PT_armorpaint_import_textures"
    bl_label = "Sync Textures"

    def draw(self, context):
        scene = context.scene
        obj = context.object
        obj_data = bpy.data.objects[context.active_object.name]
        use_custom = scene.armorpaint_properties.use_custom_texture_dir
        texture_path = Path(scene.armorpaint_properties.texture_path)

        layout = self.layout
        col = layout.split().column()

        if obj.type == "MESH":
            if "armorpaint_proj_dir" in obj_data and Path(
                obj_data["armorpaint_proj_dir"]
            ).is_dir():
                col.prop(
                    scene.armorpaint_properties,
                    "use_custom_texture_dir",
                    text="Custom Texture Directory",
                )
                if use_custom:
                    col.prop(
                        scene.armorpaint_properties,
                        "texture_path",
                        text="Directory",
                    )
                export_dir = (
                    texture_path
                    if use_custom and texture_path.is_dir()
                    else Path(obj_data["armorpaint_proj_dir"]) / "exports"
                )
                if export_dir.is_dir():
                    col.operator(
                        "object.armorpaint_livelink_textures_loader",
                        text="Load textures",
                        icon="SHADING_TEXTURE",
                    )
                else:
                    col.label(
                        text="Textures must be in a subdirectory called 'exports'"
                    )
            else:
                col.label(
                    text="Open your mesh in ArmorPaint before applying textures"
                )
        else:
            col.label(icon="CANCEL", text="Only meshes support textures!")

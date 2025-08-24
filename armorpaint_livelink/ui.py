import os
import bpy
from bpy.types import Panel

from .utils import SEP


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
    bl_label = "Open AmorPaint"

    def draw(self, context):
        scene = context.scene
        obj_type = context.active_object.type
        use_custom_filename = scene.armorpaint_properties.use_custom_filename

        layout = self.layout
        col = layout.split().column()

        if obj_type == "MESH":
            col.prop(
                scene.armorpaint_properties,
                "use_custom_filename",
                text="Custom File Name",
            )
            if use_custom_filename:
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
        obj_type = context.object.type
        obj = bpy.data.objects[context.active_object.name]

        use_custom_dir = scene.armorpaint_properties.use_custom_texture_dir
        texture_path = scene.armorpaint_properties.texture_path

        layout = self.layout
        col = layout.split().column()

        if obj_type == "MESH":
            if "armorpaint_proj_dir" in obj and os.path.isdir(
                obj["armorpaint_proj_dir"]
            ):
                col.prop(
                    scene.armorpaint_properties,
                    "use_custom_texture_dir",
                    text="Custom Texture Directory",
                )

                if use_custom_dir:
                    col.prop(
                        scene.armorpaint_properties, "texture_path", text="Directory"
                    )

                if use_custom_dir and os.path.isdir(texture_path):
                    export_dir = texture_path
                else:
                    export_dir = obj["armorpaint_proj_dir"] + SEP + "exports"

                if os.path.isdir(export_dir):
                    col.operator(
                        "object.armorpaint_livelink_textures_loader",
                        text="Load textures",
                        icon="SHADING_TEXTURE",
                    )
                else:
                    col.label(
                        text='Textures must be in a subdirectory called "exports"'
                    )
            else:
                col.label(text="Open your mesh in ArmorPaint")
                col.label(text=" before applying textures please!")
        else:
            col.label(icon="CANCEL", text="Only meshes support textures!")

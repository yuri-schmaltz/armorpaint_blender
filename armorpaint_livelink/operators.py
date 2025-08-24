"""Operators for ArmorPaint live link."""

from __future__ import annotations

import subprocess
from pathlib import Path

import bpy
from bpy.types import Operator

from .utils import generate_material


class ArmorPaintLivelinkOperator(Operator):
    bl_idname = "object.armorpaint_livelink"
    bl_label = "Export Selection to ArmorPaint"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        scene = context.scene
        prefs = context.preferences.addons[__name__].preferences
        path_exe = prefs.path_exe

        obj = context.active_object
        obj_name = obj.name
        obj_data = bpy.data.objects[obj_name]
        project_path = scene.armorpaint_properties.project_path

        if obj.type != "MESH":
            self.report({"ERROR"}, "ArmorPaint only works with meshes")
            return {"CANCELLED"}
        if not path_exe:
            self.report({"ERROR"}, "No ArmorPaint executable path in settings")
            return {"CANCELLED"}
        if not scene.armorpaint_properties:
            self.report({"ERROR"}, "Set an ArmorPaint project directory first")
            return {"CANCELLED"}
        if not bpy.data.filepath:
            self.report({"ERROR"}, "Save blend file first")
            return {"CANCELLED"}

        if "armorpaint_proj_dir" in obj_data and (
            Path(obj_data["armorpaint_proj_dir"]) / obj_data["armorpaint_filename"]
        ).is_file():
            arm_filepath = Path(obj_data["armorpaint_proj_dir"]) / obj_data[
                "armorpaint_filename"
            ]
            subprocess.Popen([path_exe, str(arm_filepath)])
        else:
            path_tmp = Path(bpy.path.abspath(project_path)) / "tmp.obj"
            bpy.ops.export_scene.obj(
                filepath=str(path_tmp),
                check_existing=True,
                axis_forward="-Z",
                axis_up="Y",
                filter_glob="*.obj;*.mtl",
                use_selection=True,
                use_animation=False,
                use_mesh_modifiers=True,
                use_edges=True,
                use_smooth_groups=True,
                use_smooth_groups_bitflags=False,
                use_normals=True,
                use_uvs=True,
                use_materials=True,
                use_triangles=False,
                use_nurbs=False,
                use_vertex_groups=False,
                use_blen_objects=True,
                group_by_object=False,
                group_by_material=False,
                keep_vertex_order=False,
                global_scale=1,
                path_mode="AUTO",
            )
            subprocess.Popen([path_exe, str(path_tmp)])
            obj_data["armorpaint_proj_dir"] = str(
                Path(bpy.path.abspath(project_path)).resolve()
            )
            obj_data["armorpaint_filename"] = f"{obj_name}.arm"
        return {"FINISHED"}


class ArmorPaintLivelinkTexturesLoaderOperator(Operator):
    bl_idname = "object.armorpaint_livelink_textures_loader"
    bl_label = "ArmorPaint Live-Link - Load Textures"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        scene = context.scene
        obj_data = bpy.data.objects[context.active_object.name]
        use_custom_dir = scene.armorpaint_properties.use_custom_texture_dir
        texture_path = Path(scene.armorpaint_properties.texture_path)

        if use_custom_dir and texture_path.is_dir():
            generate_material(texture_path)
        else:
            generate_material(Path(obj_data["armorpaint_proj_dir"]) / "exports")
        return {"FINISHED"}

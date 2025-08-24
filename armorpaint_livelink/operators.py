import os
import subprocess
import bpy
from bpy.types import Operator

from .utils import generate_material, SEP


class ArmorPaintLiveLinkOperator(Operator):
    """Export the selected object to ArmorPaint."""

    bl_idname = "object.armorpaint_livelink"
    bl_label = "Export Selection to ArmorPaint"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        scene = context.scene
        prefs = context.preferences.addons[__package__].preferences
        path_exe = prefs.path_exe

        obj_type = context.active_object.type
        obj_name = context.active_object.name
        obj = bpy.data.objects[obj_name]

        project_path = scene.armorpaint_properties.project_path

        if obj_type != "MESH":
            self.report({"ERROR"}, "ArmorPaint only works with meshes")
            return {"CANCELLED"}
        if path_exe == "":
            self.report({"ERROR"}, "No ArmorPaint executable path in settings")
            return {"CANCELLED"}
        if scene.armorpaint_properties == "":
            self.report({"ERROR"}, "Set an ArmorPaint project directory first")
            return {"CANCELLED"}
        if bpy.data.filepath == "":
            self.report({"ERROR"}, "Save blend file first")
            return {"CANCELLED"}

        if "armorpaint_proj_dir" in obj and os.path.isfile(
            obj["armorpaint_proj_dir"] + SEP + obj["armorpaint_filename"]
        ):
            arm_filepath = obj["armorpaint_proj_dir"] + SEP + obj["armorpaint_filename"]
            subprocess.Popen([path_exe, arm_filepath])
        else:
            tmp_path = bpy.path.abspath(project_path) + SEP + "tmp.obj"
            bpy.ops.export_scene.obj(
                filepath=tmp_path,
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

            subprocess.Popen([path_exe, tmp_path])

            obj["armorpaint_proj_dir"] = os.path.realpath(
                bpy.path.abspath(project_path)
            )
            obj["armorpaint_filename"] = f"{obj_name}.arm"

        return {"FINISHED"}


class ArmorPaintLiveLinkTexturesLoaderOperator(Operator):
    """Load textures exported from ArmorPaint and create a material."""

    bl_idname = "object.armorpaint_livelink_textures_loader"
    bl_label = "ArmorPaint Live-Link - Load Textures"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        scene = context.scene
        obj = bpy.data.objects[context.active_object.name]
        use_custom_dir = scene.armorpaint_properties.use_custom_texture_dir
        texture_path = scene.armorpaint_properties.texture_path

        if use_custom_dir and os.path.isdir(texture_path):
            generate_material(texture_path)
        else:
            generate_material(obj["armorpaint_proj_dir"] + SEP + "exports")

        return {"FINISHED"}


    bl_idname = "object.armorpaint_livelink"
    bl_label = "Export Selection to ArmorPaint"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        scene = context.scene

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

    bl_idname = "object.armorpaint_livelink_textures_loader"
    bl_label = "ArmorPaint Live-Link - Load Textures"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        scene = context.scene

        return {"FINISHED"}

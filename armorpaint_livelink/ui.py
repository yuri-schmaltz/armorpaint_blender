

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

            col.prop(
                scene.armorpaint_properties,
                "use_custom_filename",
                text="Custom File Name",
            )

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


        layout = self.layout
        col = layout.split().column()


                col.prop(
                    scene.armorpaint_properties,
                    "use_custom_texture_dir",
                    text="Custom Texture Directory",
                )

                    col.operator(
                        "object.armorpaint_livelink_textures_loader",
                        text="Load textures",
                        icon="SHADING_TEXTURE",
                    )
                else:
                    col.label(

        else:
            col.label(icon="CANCEL", text="Only meshes support textures!")

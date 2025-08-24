
    textures = search_textures(path, textures)

    if "ArmorPaintMtl" in bpy.data.materials:
        reload_textures()
        return

    material = bpy.data.materials.new(name="ArmorPaintMtl")
    material.use_nodes = True

    material_output = material.node_tree.nodes.get("Material Output")
    principled_node = material.node_tree.nodes.get("Principled BSDF")


    bpy.context.object.active_material = material

import os
import platform
import bpy

SYSTEM = platform.system()
SEP = os.sep


def search_textures(path, textures):
    """Populate the textures list with texture paths found in *path*."""
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".hdr", ".exr")
        ):
            if "_base" in filename:
                textures[0] = file_path
            if "_subs" in filename:
                textures[1] = file_path
            if "_metal" in filename:
                textures[2] = file_path
            if "_rough" in filename:
                textures[3] = file_path
            if "_emission" in filename:
                textures[4] = file_path
            if "_opac" in filename:
                textures[5] = file_path
            if "_nor" in filename:
                textures[6] = file_path
    return textures


def reload_textures():
    """Reload all file-based images and remove unused ones."""
    for image in bpy.data.images:
        if not image.users:
            bpy.data.images.remove(image)

    for image in bpy.data.images:
        if image.source == "FILE":
            image.reload()


def generate_material(path):
    """Create a material using textures found in *path*."""
    textures = [None] * 7
    textures = search_textures(path, textures)

    if "ArmorPaintMtl" in bpy.data.materials:
        reload_textures()
        return

    material = bpy.data.materials.new(name="ArmorPaintMtl")
    material.use_nodes = True

    material_output = material.node_tree.nodes.get("Material Output")
    principled_node = material.node_tree.nodes.get("Principled BSDF")

    diff_texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    diff_texture.name = "diffuse_texture"
    diff_texture.location = -460, 820.0
    if textures[0] is not None:
        diff_texture.image = bpy.data.images.load(filepath=textures[0])

    subs_texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    subs_texture.name = "subsurface_texture"
    subs_texture.location = -460, 540.0
    if textures[1] is not None:
        subs_texture.image = bpy.data.images.load(filepath=textures[1])

    metallic_texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    metallic_texture.name = "metallic_texture"
    metallic_texture.location = -460, 260.0
    if textures[2] is not None:
        metallic_texture.image = bpy.data.images.load(filepath=textures[2])

    roughness_texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    roughness_texture.name = "roughness_texture"
    roughness_texture.location = -460, -20.0
    if textures[3] is not None:
        roughness_texture.image = bpy.data.images.load(filepath=textures[3])

    emission_texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    emission_texture.name = "emission_texture"
    emission_texture.location = -460, -300.0
    if textures[4] is not None:
        emission_texture.image = bpy.data.images.load(filepath=textures[4])

    opacity_texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    opacity_texture.name = "opacity_texture"
    opacity_texture.location = -460, -580.0
    if textures[5] is not None:
        opacity_texture.image = bpy.data.images.load(filepath=textures[5])

    normal_texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    normal_texture.name = "normal_texture"
    normal_texture.location = -460, -860.0
    if textures[6] is not None:
        normal_texture.image = bpy.data.images.load(filepath=textures[6])

    normal_node = material.node_tree.nodes.new("ShaderNodeNormalMap")
    normal_node.location = -200.0, -860.0

    mapping_node = material.node_tree.nodes.new("ShaderNodeMapping")
    mapping_node.location = -640.0, 200.0
    coord_node = material.node_tree.nodes.new("ShaderNodeTexCoord")
    coord_node.location = -800.0, 200.0

    links = material.node_tree.links
    links.new(material_output.inputs["Surface"], principled_node.outputs["BSDF"])

    if textures[0] is not None:
        links.new(principled_node.inputs["Base Color"], diff_texture.outputs["Color"])
    if textures[1] is not None:
        links.new(
            principled_node.inputs["Subsurface Color"], subs_texture.outputs["Color"]
        )
    if textures[2] is not None:
        links.new(principled_node.inputs["Metallic"], metallic_texture.outputs["Color"])
    if textures[3] is not None:
        links.new(
            principled_node.inputs["Roughness"], roughness_texture.outputs["Color"]
        )
    if textures[4] is not None:
        links.new(principled_node.inputs["Emission"], emission_texture.outputs["Color"])
    if textures[5] is not None:
        links.new(principled_node.inputs["Alpha"], opacity_texture.outputs["Color"])

    links.new(normal_node.inputs["Color"], normal_texture.outputs["Color"])
    links.new(principled_node.inputs["Normal"], normal_node.outputs["Normal"])

    links.new(diff_texture.inputs["Vector"], mapping_node.outputs["Vector"])
    links.new(subs_texture.inputs["Vector"], mapping_node.outputs["Vector"])
    links.new(metallic_texture.inputs["Vector"], mapping_node.outputs["Vector"])
    links.new(roughness_texture.inputs["Vector"], mapping_node.outputs["Vector"])
    links.new(emission_texture.inputs["Vector"], mapping_node.outputs["Vector"])
    links.new(opacity_texture.inputs["Vector"], mapping_node.outputs["Vector"])
    links.new(normal_texture.inputs["Vector"], mapping_node.outputs["Vector"])

    links.new(mapping_node.inputs["Vector"], coord_node.outputs["UV"])

    bpy.context.object.active_material = material

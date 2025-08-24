"""Utility functions for ArmorPaint live link."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

TEXTURE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tiff",
    ".bmp",
    ".hdr",
    ".exr",
}


def search_textures(path: Path, textures: List[Optional[str]]) -> List[Optional[str]]:
    """Search for texture files in *path* and fill *textures* list.

    The list order is: base color, subsurface, metallic, roughness,
    emission, opacity and normal map.
    """

    for file in path.iterdir():
        if file.is_file() and file.suffix.lower() in TEXTURE_EXTENSIONS:
            name = file.stem.lower()
            file_str = str(file)
            if "_base" in name:
                textures[0] = file_str
            if "_subs" in name:
                textures[1] = file_str
            if "_metal" in name:
                textures[2] = file_str
            if "_rough" in name:
                textures[3] = file_str
            if "_emission" in name:
                textures[4] = file_str
            if "_opac" in name:
                textures[5] = file_str
            if "_nor" in name:
                textures[6] = file_str
    return textures


def reload_textures() -> None:
    """Reload all file based images and remove unused ones."""

    import bpy

    for img in list(bpy.data.images):
        if not img.users:
            bpy.data.images.remove(img)

    for img in bpy.data.images:
        if img.source == "FILE":
            img.reload()


def generate_material(path: Path) -> None:
    """Create or update the material from texture files located in *path*."""

    import bpy

    textures: List[Optional[str]] = [None] * 7
    textures = search_textures(path, textures)

    if "ArmorPaintMtl" in bpy.data.materials:
        reload_textures()
        return

    material = bpy.data.materials.new(name="ArmorPaintMtl")
    material.use_nodes = True

    material_output = material.node_tree.nodes.get("Material Output")
    principled_node = material.node_tree.nodes.get("Principled BSDF")

    link_nodes = material.node_tree.links

    def _add_tex_node(name: str, location: tuple, image_path: Optional[str]):
        node = material.node_tree.nodes.new("ShaderNodeTexImage")
        node.name = name
        node.location = location
        if image_path:
            node.image = bpy.data.images.load(filepath=image_path)
        return node

    diff_texture = _add_tex_node("diffuse_texture", (-460, 820.0), textures[0])
    subs_texture = _add_tex_node("subsurface_texture", (-460, 540.0), textures[1])
    metallic_texture = _add_tex_node("metallic_texture", (-460, 260.0), textures[2])
    roughness_texture = _add_tex_node("roughness_texture", (-460, -20.0), textures[3])
    emission_texture = _add_tex_node("emission_texture", (-460, -300.0), textures[4])
    opacity_texture = _add_tex_node("opacity_texture", (-460, -580.0), textures[5])
    normal_texture = _add_tex_node("normal_texture", (-460, -860.0), textures[6])

    normal_node = material.node_tree.nodes.new("ShaderNodeNormalMap")
    normal_node.location = (-200.0, -860.0)

    mapping_node = material.node_tree.nodes.new("ShaderNodeMapping")
    mapping_node.location = (-640.0, 200.0)
    coord_node = material.node_tree.nodes.new("ShaderNodeTexCoord")
    coord_node.location = (-800.0, 200.0)

    link_nodes.new(material_output.inputs["Surface"], principled_node.outputs["BSDF"])

    if textures[0]:
        link_nodes.new(
            principled_node.inputs["Base Color"],
            diff_texture.outputs["Color"],
        )
    if textures[1]:
        link_nodes.new(
            principled_node.inputs["Subsurface Color"],
            subs_texture.outputs["Color"],
        )

    if textures[2]:
        link_nodes.new(
            principled_node.inputs["Metallic"],
            metallic_texture.outputs["Color"],
        )
    if textures[3]:
        link_nodes.new(
            principled_node.inputs["Roughness"],
            roughness_texture.outputs["Color"],
        )
    if textures[4]:
        link_nodes.new(
            principled_node.inputs["Emission"],
            emission_texture.outputs["Color"],
        )
    if textures[5]:
        link_nodes.new(
            principled_node.inputs["Alpha"],
            opacity_texture.outputs["Color"],
        )

    link_nodes.new(normal_node.inputs["Color"], normal_texture.outputs["Color"])
    link_nodes.new(principled_node.inputs["Normal"], normal_node.outputs["Normal"])

    for node in (
        diff_texture,
        subs_texture,
        metallic_texture,
        roughness_texture,
        emission_texture,
        opacity_texture,
        normal_texture,
    ):
        link_nodes.new(node.inputs["Vector"], mapping_node.outputs["Vector"])

    link_nodes.new(mapping_node.inputs["Vector"], coord_node.outputs["UV"])

    bpy.context.object.active_material = material

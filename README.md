# ArmorPaint Blender Live-Link

Blender add-on for [ArmorPaint](https://armorpaint.org/). This is a fork of the awesome [Blender-ArmorPaintLiveLink](https://github.com/PiloeGAO/Blender-ArmorPaintLiveLink) repository by PiloeGAO with the goal to keep it under active development.

## Prerequisites
- [ArmorPaint 0.9](https://armorpaint.org/download)
- [Blender 3.6](https://www.blender.org/download/)

## Installation
1. Download `armorpaint_blender.zip` from the [releases](https://github.com/armory3d/armorpaint_blender/releases) page.
2. Extract `armorpaint_blender.zip`.
3. In Blender, press **Edit > Preferences... > Add-ons > Install...** and select the `armorpaint_livelink` directory.
4. Enable the add-on.
5. In the add-on preferences, set the path to your ArmorPaint executable.

## Usage
1. In the 3D View, open the side panel (`N` shortcut) and locate the project directory (folder where your `.arm` file and textures will be saved).
2. Select your unwrapped object and click **Open in ArmorPaint**.
3. Texture in ArmorPaint. When done, export your textures to a subdirectory called `exports`.
4. Back in Blender, use **Sync Textures** to load the exported textures into a new material.

## Contributing
Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code style and development process.

## License
Distributed under the GNU General Public License v3. See [LICENSE](LICENSE) for more information.

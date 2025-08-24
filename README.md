# armorpaint_blender

Blender add-on for [ArmorPaint](https://armorpaint.org/). Fork of the awesome [Blender-ArmorPaintLiveLink](https://github.com/PiloeGAO/Blender-ArmorPaintLiveLink) repo by PiloeGAO with the goal to keep it under active development.

## Installation

- Get ArmorPaint 0.9 and Blender 3.6.
- Download `armorpaint_blender.zip` from [Releases](https://github.com/armory3d/armorpaint_blender/releases).
- Extract `armorpaint_blender.zip`.
- In Blender press *Edit > Preferences... > Add-ons > Install...* and select the `armorpaint_livelink` folder or the zipped add-on.
- Enable the add-on.
- In the add-on preferences point the **ArmorPaint Executable** field to your ArmorPaint binary.
- In the 3D View, open the side panel (*N* shortcut) and locate the project directory (folder where your `.arm` file and textures will be saved).
- Select your object (needs to be unwrapped) and click on **Open in ArmorPaint**.
- When the texturing process is done, export your textures to a subdirectory called `exports`.

## Development

The add-on code is split into several modules:

- `operators.py` – operators for exporting meshes and loading textures.
- `properties.py` – add-on preferences and scene properties.
- `ui.py` – user interface panels.
- `utils.py` – shared utility helpers.

Set up the development environment:

```bash
python -m pip install -r requirements-dev.txt
flake8
pytest
```

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on our coding guidelines and development workflow.

## Roadmap

Planned features and ideas can be found in [ROADMAP.md](ROADMAP.md).

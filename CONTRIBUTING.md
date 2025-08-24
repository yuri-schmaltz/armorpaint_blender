# Contributing

Thanks for your interest in contributing! Please follow these guidelines when submitting patches:

## Development setup
1. Ensure you have Python 3.10 or newer installed.
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
   (Currently only `flake8` is required.)

## Code style
- Run `black .` before committing code.
- Lint the code with `flake8`.
- Follow [PEP 8](https://peps.python.org/pep-0008/) naming conventions and write docstrings for new functions and classes.

## Testing
- Run `python -m py_compile armorpaint_livelink/*.py` to ensure modules compile.

Please open a pull request with a clear description of your changes.

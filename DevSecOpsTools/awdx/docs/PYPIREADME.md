# Publishing awdx to PyPI

This guide explains how to publish (or update) the awdx package and its README on [PyPI](https://pypi.org/).

---

## 1. Update Your README (Optional)
Edit your `README.md` as needed. This file will be displayed as your project description on PyPI.

---

## 2. Bump the Version
PyPI does **not** allow re-uploading the same version. You must increment the version number in your `pyproject.toml` or `setup.py`:

- For `pyproject.toml`:
  ```toml
  version = "0.0.1"  # Update to a new version
  ```
- For `setup.py`:
  ```python
  version="0.0.1",
  ```

---

## 3. Clean Previous Builds
Remove old build artifacts to avoid confusion:
```bash
rm -rf dist/ build/ *.egg-info
```

---

## 4. Build the Package
Use the `build` module to create distribution files:
```bash
python3 -m pip install --upgrade build
python3 -m build
```
This will create files in the `dist/` directory.

---

## 5. Upload to PyPI
Use `twine` to upload your package:
```bash
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```
- You will be prompted for your PyPI username and password (or API token).

---

## 6. Verify on PyPI
Go to [https://pypi.org/project/awdx/](https://pypi.org/project/awdx/) and check that your new version and README are visible.

---

## Notes
- **You cannot update only the README on PyPI.** Any change to the README requires a new package version and a full re-upload.
- If you see an error like `File already exists`, you must increment the version number.
- For more details, see the [PyPI documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

---

## Example: Full Workflow
```bash
# 1. Edit README.md and bump version in pyproject.toml

# 2. Clean old builds
rm -rf dist/ build/ *.egg-info

# 3. Build
python3 -m build

# 4. Upload
python3 -m twine upload dist/*
``` 
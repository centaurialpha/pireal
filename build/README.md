# Building Pireal

## Requirements

### Linux
- Arch Linux (GLIBC 2.38+)
- `uv`
- FUSE (available by default on Arch)

### Windows
- Windows 10/11 x86_64
- Python 3.12 from python.org (add to PATH)
- `uv` -> `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- [Inno Setup 6](https://jrsoftware.org/isdl.php) at default install path

## Pre-release checklist

```bash
# 1. Working tree must be clean
git status   # "nothing to commit, working tree clean"

# 2. Tag the release
git tag -a v4.0.0 -m "Release v4.0.0"

# 3. Refresh version
uv sync --reinstall-package pireal
uv run python -c "from importlib.metadata import version; print(version('pireal'))"

# 4. Push tag
git push origin v4.0.0
```

## Build

```bash
# Full build
uv run python build/build.py

# Skip Nuitka recompilation (rebuild package only)
uv run python build/build.py --skip-nuitka
```

### Output

| Platform | Artifact |
|----------|----------|
| Linux    | `dist/Pireal-4.0.0-x86_64.AppImage` |
| Windows  | `dist/Pireal-4.0.0-windows-x86_64-setup.exe` |

## Notes

- First build takes ~5 min (Nuitka compiles C backend). Install `ccache` to speed up rebuilds:
  ```bash
  sudo pacman -S ccache   # Arch
  ```
- `appimagetool` is downloaded automatically to `build/linux/` on first Linux build.
- `build/windows/installer.iss` is generated automatically — do not edit it directly, edit `installer.iss.in`.
- Both `dist/` and `build/linux/appimagetool` are in `.gitignore`.

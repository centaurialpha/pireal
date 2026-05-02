# Building Pireal AppImage (Linux x86_64)

## Requirements
- Arch Linux (or any distro with GLIBC 2.38+)
- `uv`
- `nuitka` (included as dev dep)
- FUSE (for appimagetool, available by default en Arch)

## Steps

### 1. Ensure clean working tree
```
git status   # must show "nothing to commit, working tree clean"
```

### 2. Tag the release
```
git tag -a v4.0.0 -m "Release v4.0.0"
```

### 3. Refresh version
```
uv sync --reinstall-package pireal
uv run python -c "from importlib.metadata import version; print(version('pireal'))"
```
# -> 4.0.0

### 4. Build
```
uv run python build/linux/build_appimage.py
```

# To skip Nuitka recompilation (rebuild AppDir/AppImage only):
```
uv run python build/linux/build_appimage.py --skip-nuitka
```

### 5. Output
dist/Pireal-4.0.0-x86_64.AppImage

### Notes
- First build takes ~5 min (Nuitka compiles 400 C files)
- Install ccache for faster rebuilds: sudo pacman -S ccache
- appimagetool is downloaded automatically to build/linux/ on first run

# Deployment & Distribution Options

## 1. Docker Container (Recommended for CI/CD)

Docker is great for running this tool in CI/CD pipelines (like GitHub Actions) or ensuring a consistent environment.

### How to Build
```bash
docker build -t codeinspector .
```

### How to Run
Since this tool needs to access your **local git repository**, you must mount your current directory into the container.

```bash
# Run commit command
docker run --rm -it \
  -v $(pwd):/app \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  codeinspector commit

# Run PR command
docker run --rm -it \
  -v $(pwd):/app \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  codeinspector pr --title "My Feature" --auto
```

**Pros:**
- No Python installation required for the user.
- Consistent environment (same versions of dependencies).

**Cons:**
- Command is verbose (requires `-v` volume mounting).
- Slower startup than a native binary.

---

## 2. Python Package (PyPI) - Best for Developers

The most natural way for developers to use this is via `pip`.

### Setup
1. Create `setup.py` (or `pyproject.toml`).
2. Build and publish to PyPI.

### User Experience
```bash
pip install codeinspector-ai
codeinspector commit
```

**Pros:**
- Native feel.
- Easy to update (`pip install --upgrade`).

**Cons:**
- Requires Python installed on user's machine.

---

## 3. Standalone Executable (PyInstaller)

Compile the app into a single `.exe` (Windows) or binary (Mac/Linux).

### Setup
```bash
pip install pyinstaller
pyinstaller --onefile codeinspector/cli.py --name codeinspector
```

### User Experience
Download `codeinspector.exe` and run it directly.

**Pros:**
- No dependencies (Python not required).
- Fast execution.

**Cons:**
- Need to build separate binaries for Windows, Mac, and Linux.

---

## Recommendation

1. **For Local Use:** Publish as a **Python Package (PyPI)**. It offers the best DX for developers.
2. **For CI/CD:** Use the **Docker Image**. It's perfect for automated pipelines.

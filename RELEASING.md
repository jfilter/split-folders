# Releasing

## Version locations

The version string lives in two places and **both must be updated**:

- `pyproject.toml` &rarr; `version = "X.Y.Z"`
- `splitfolders/__init__.py` &rarr; `__version__ = "X.Y.Z"`

## Steps

1. **Update the version** in both files listed above.

2. **Commit the version bump:**

   ```bash
   git add pyproject.toml splitfolders/__init__.py
   git commit -m "Bump version to X.Y.Z"
   ```

3. **Create a git tag:**

   ```bash
   git tag X.Y.Z
   ```

4. **Push the commit and tag:**

   ```bash
   git push && git push --tags
   ```

5. **Build and publish to PyPI:**

   ```bash
   poetry build
   poetry publish
   ```

   This requires PyPI credentials configured locally via `poetry config pypi-token.pypi <token>`.

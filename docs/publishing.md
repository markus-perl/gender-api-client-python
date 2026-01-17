# Publishing `gender-api-client` to PyPI

This guide will walk you through the process of publishing your Python package to the Python Package Index (PyPI).

## 1. Prerequisites

Before you begin, make sure you have:

1.  **A PyPI Account**: Register at [pypi.org](https://pypi.org/account/register/).
2.  **An API Token**: Go to [Account Settings](https://pypi.org/manage/account/) on PyPI and create a "New API token". 
    > [!IMPORTANT]
    > Save this token safely. You will use it instead of your password.

## 2. Prepare Your Environment

Install the necessary tools for building and uploading packages:

```bash
pip install --upgrade build twine
```

## 3. Build the Package

From the root of your project (where `pyproject.toml` is located), run:

```bash
python3 -m build
```

This will create a `dist/` directory containing:
- A `.tar.gz` file (Source Distribution).
- A `.whl` file (Built Distribution/Wheel).

## 4. Verify the Build

You can check if the generated files are valid using `twine`:

```bash
twine check dist/*
```

## 5. Upload to TestPyPI (Optional but Recommended)

TestPyPI is a separate instance of PyPI for testing. It allows you to verify the upload without affecting the real index.

1.  **Register** at [test.pypi.org](https://test.pypi.org/account/register/).
2.  **Upload**:
    ```bash
    twine upload --repository testpypi dist/*
    ```
    (Use `__token__` as the username and your TestPyPI API token as the password.)

3.  **Verify**: Try installing it in a fresh virtual environment:
    ```bash
    pip install --index-url https://test.pypi.org/simple/ --no-deps gender-api-client
    ```

## 6. Upload to PyPI

Once you are confident, upload to the official PyPI:

```bash
twine upload dist/*
```

- **Username**: `__token__`
- **Password**: Your PyPI API token (including the `pypi-` prefix).

## 7. Versioning

Whenever you want to release a new version:
1.  Update the `version` field in `pyproject.toml`.
2.  Commit the change and tag it: `git tag v1.1.0`.
3.  Repeat the **Build** and **Upload** steps.

---

### Pro Tip: Automate with GitHub Actions

You can automate this process using GitHub Actions so that every time you push a tag, the package is automatically published.

Add a new workflow file `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

*Note: You would need to add `PYPI_API_TOKEN` to your GitHub repository secrets.*

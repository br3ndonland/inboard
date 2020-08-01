# Python template repository

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
![hooks](https://github.com/br3ndonland/template-python/workflows/hooks/badge.svg)
![tests](https://github.com/br3ndonland/template-python/workflows/tests/badge.svg)

Brendon Smith ([br3ndonland](https://github.com/br3ndonland/))

## Description

**Welcome!** This is a template repository for Python projects, engineered for use as a [GitHub template repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template). To use the template, click on "Use this template" or browse to [template-python/generate](https://github.com/br3ndonland/template-python/generate). GitHub will create a new repository without the commit history from this one.

Another common approach, especially for Python, is to use [cookiecutter](https://github.com/cookiecutter/cookiecutter). In a cookiecutter repo, the developer adds template variables throughout, like `{{cookiecutter.repo_name}}`. When a user runs `cookiecutter` using the template repository, the template variables are replaced with the information the user provides.

This repo is simple enough that I haven't needed to add cookiecutter yet. The `template-python` repo name can be replaced with a one-line terminal command: `git grep -l 'template-python' | xargs sed -i '' 's/template-python/repo-name/g'` (replace `repo-name` with the name of the repository you generate). There may also be a few edits to the _pyproject.toml_ needed. See the [quickstart](#quickstart) section for more.

## Quickstart

```sh
❯ cd path/to/repo
# Replace instances of template-python with new repo name
# In the command below, use your repo name instead of 'repo-name'
❯ git grep -l 'template-python' | xargs sed -i '' 's|template-python|repo-name|g'
❯ git grep -l 'templatepython' | xargs sed -i '' 's|templatepython|repo-name|g'
# Install virtual environment with poetry: https://python-poetry.org/docs/
❯ poetry install
❯ poetry shell
# Install pre-commit hooks
.venv ❯ pre-commit install
# Try running the tests
.venv ❯ pytest
```

## Further information

See [CONTRIBUTING.md](.github/CONTRIBUTING.md).

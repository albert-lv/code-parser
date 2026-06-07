# Contributing to Code Parser

Thanks for your interest in contributing! This document provides guidelines for bug reports, feature requests, and pull requests.

## How to Contribute

1. **Fork** the repository and clone your fork.
2. **Create a branch** for your change:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and add or update tests where applicable.
4. **Run the test suite** and ensure everything passes:
   ```bash
   python -m pytest
   ```
5. **Commit** with a clear message following conventional commits:
   ```bash
   git commit -m "feat: add support for parsing @PatchMapping"
   ```
6. **Push** to your fork and open a Pull Request.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Keep functions focused and under 50 lines when possible.
- Add docstrings to public functions and modules.
- Write clear variable names.

## Reporting Bugs

When reporting a bug, please include:
- A clear description of the problem.
- Steps to reproduce.
- Expected vs. actual behavior.
- Python version and operating system.
- Sample code or diff that triggers the issue.

## Adding New Languages

To add support for a new tree-sitter language:
1. Add the grammar as a git submodule in `vendor/`.
2. Update `init_library.py` to include the new language.
3. Run `python init_library.py` to rebuild `language/my-languages.so`.
4. Add parsing logic and tests.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

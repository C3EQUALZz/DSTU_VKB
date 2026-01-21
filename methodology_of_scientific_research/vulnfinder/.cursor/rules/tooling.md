## Tooling & Standards (Mandatory)

- Python **3.12**
- Task runner: `just` and `pre-commit`
- Formatting & linting: **Ruff**
- Type checking: **mypy**
- Testing: **pytest** with coverage
- All code must be **fully type annotated**
- Try not to use **typing.Any**

Common commands:
```sh
just pre-commit-all
just ruff-check
just ruff-format
pytest -v
```

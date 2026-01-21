# Cross-platform shell configuration
# Use PowerShell on Windows (higher precedence than shell setting)
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
# Use sh on Unix-like systems
set shell := ["sh", "-c"]


[doc("All command information")]
default:
  @just --list --unsorted --list-heading $'Dishka-jobify  commands…\n'

# Linter
[doc("Ruff format")]
[group("linter")]
ruff-format *params:
  uv run --active --frozen ruff format {{params}}

[doc("Ruff check")]
[group("linter")]
ruff-check *params:
  uv run --active --frozen ruff check --exit-non-zero-on-fix {{params}}

_codespell:
  uv run --active --frozen codespell -L Dependant,dependant

[doc("Check typos")]
[group("linter")]
typos: _codespell
  uv run --active --frozen prek run --all-files typos

alias lint := linter

[doc("Linter run")]
[group("linter")]
linter: ruff-format ruff-check _codespell

# Static analysis
[doc("Mypy check")]
[group("static analysis")]
mypy *params:
  uv run --active --frozen mypy {{params}}

[doc("Bandit check")]
[group("static analysis")]
bandit:
  uv run --active --frozen bandit -c pyproject.toml -r src

[doc("Semgrep check")]
[group("static analysis")]
semgrep:
  uv run --active --frozen semgrep scan --config auto --error --skip-unknown-extensions src

[doc("Zizmor check")]
[group("static analysis")]
zizmor:
  uv run --active --frozen zizmor .

[doc("Static analysis check")]
[group("static analysis")]
static-analysis: mypy bandit semgrep

[doc("Install pre-commit hooks")]
[group("pre-commit")]
pre-commit-install:
  uv run --active --frozen prek install

[doc("Pre-commit modified files")]
[group("pre-commit")]
pre-commit:
  uv run --active --frozen prek run

[doc("Pre-commit all files")]
[group("pre-commit")]
pre-commit-all:
  uv run --active --frozen prek run --all-files
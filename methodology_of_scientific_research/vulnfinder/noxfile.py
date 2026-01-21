import nox


nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True


PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14"]


def install_command(dependency: str, version: str | None = None) -> str:
    """Return install command for a specific dependency."""
    return f"{dependency}=={version}" if version else dependency


def load_test_dependencies() -> list[str]:
    """Load development dependencies from pyproject.toml."""
    toml_data = nox.project.load_toml("pyproject.toml")
    return toml_data["dependency-groups"]["test"]


@nox.session()
@nox.parametrize("python", PYTHON_VERSIONS)
def tests(
    session: nox.Session,
    python: str,
) -> None:
    """Run tests with different versions of Python and dependencies."""

    dev_deps = load_test_dependencies()
    session.install(*dev_deps)

    session.install("-e", ".")

    session.run(
        "pytest",
        "tests",
        "--cov=dishka_jobify",
        "--cov-report=term-missing",
        "--cov-append",
        "--cov-config=.coveragerc",
        env={
            "COVERAGE_FILE": f".coverage.{session.name}",
        },
        *session.posargs,
    )


@nox.session
def coverage(session: nox.Session) -> None:
    """Generate and view coverage report."""
    session.install("coverage")
    session.run("coverage", "combine")
    session.run("coverage", "report", "--fail-under=80")
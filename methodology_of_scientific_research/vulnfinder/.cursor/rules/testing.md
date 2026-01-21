## Testing Rules (Mandatory)

- Tests mirror `src/` structure
- Use `unit/`, `integration/`, `e2e/`
- Use **Arrange / Act / Assert** with explicit comments
- Do not add comments in tests except parametrization case descriptions
- Name tests by behavior and expected outcome
- Prefer unit tests; add integration tests when behavior spans layers
- Keep tests deterministic, fast, and isolated from network/IO

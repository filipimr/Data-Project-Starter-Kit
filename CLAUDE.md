# CLAUDE.md

Guidance for Claude Code (claude.ai/code) working in this repository.

## What this is

- Public template repo for bootstrapping Python data projects (ETL, ML,
  API, dashboard) with uv, Ruff, pytest, MkDocs, pre-commit, and CI
  pre-wired.
- Read `docs/guia-boas-praticas.md` for the *why* behind every convention
  here, with links to each tool's official docs.
- `app/pipeline/{extract,transform,load}.py` are placeholders
  (`raise NotImplementedError` + TODO). Don't implement them
  speculatively — this repo IS the template, not a finished pipeline.

## Commands

```bash
uv sync                        # install deps
uv run task format              # ruff check --fix . && ruff format .
uv run task lint                # ruff check . && ruff format --check .
uv run task test                # pytest -v
uv run task docs                # mkdocs serve
uv run mkdocs build --strict    # verify docs build clean
uv run pre-commit run --all-files
```

Single test: `uv run pytest tests/test_transform.py -k test_name`.

`uv run python app/main.py` raises `NotImplementedError` by design. Don't
"fix" that — it's the template's placeholder state.

## Architecture

- `app/` imports as a plain top-level package: `[tool.uv] package = false`
  in `pyproject.toml`, no wheel build, pytest rootdir insertion resolves
  `app.*` imports. Don't reintroduce `[build-system]`/hatchling without a
  reason — it broke `uv sync` before (required a README at build time).
- `docs/pipeline.md` renders live from `app/pipeline` docstrings via
  mkdocstrings. Edit the docstring, not the doc page.
- `mkdocs.yml`'s `!!python/name:` tag breaks pre-commit's `check-yaml`
  safe loader — it's excluded from that hook on purpose, not a bug.
- Ruff: `select = ["E","F","I","D","UP","B","S"]`, Google docstrings.
  `tests/*` is exempt from `D`/`S101`.

## Git workflow

- Never run `git commit --no-verify`. Fix what the hook flags instead.
- One commit/PR per concern, in adoption order: environment → code →
  tests → lint/tasks → docs → hooks/CI. No "fix everything" commits.
- Filling in a placeholder: replace one `TODO` and un-skip its matching
  test in the same change. Don't rewrite the whole pipeline at once.

## Code style

- Functions: 4-20 lines. Split if longer.
- Files: under 500 lines. Split by responsibility.
- One thing per function, one responsibility per module (SRP).
- Names: specific and unique. Avoid `data`, `handler`, `Manager`.
  Prefer names that return <5 grep hits in the codebase.
- Types: explicit. No `any`, no `Dict`, no untyped functions.
- No code duplication. Extract shared logic into a function/module.
- Early returns over nested ifs. Max 2 levels of indentation.
- Exception messages must include the offending value and expected shape.

## Comments

- Keep your own comments. Don't strip them on refactor — they carry
  intent and provenance.
- Write WHY, not WHAT. Skip `// increment counter` above `i++`.
- Docstrings on public functions: intent + one usage example.
- Reference issue numbers / commit SHAs when a line exists because
  of a specific bug or upstream constraint.

## Tests

- Tests run with a single command: `uv run pytest -v` (or
  `uv run task test`).
- Every new function gets a test. Bug fixes get a regression test.
- Mock external I/O (API, DB, filesystem) with named fake classes,
  not inline stubs.
- Tests must be F.I.R.S.T: fast, independent, repeatable,
  self-validating, timely.

## Dependencies

- Inject dependencies through constructor/parameter, not global/import.
- Wrap third-party libs behind a thin interface owned by this project.

## Structure

- `app/` holds all code, `tests/` mirrors it, `docs/` is MkDocs. If a
  framework (Django, FastAPI, Next.js...) sits on top, follow its own
  convention inside `app/`.
- Prefer small focused modules over god files.
- Predictable paths: controller/model/view, src/lib/test, etc.

## Formatting

- Use the project formatter: `uv run ruff format .`. Don't discuss style
  beyond that.

## Logging

- Structured JSON when logging for debugging / observability.
- Plain text only for user-facing CLI output.

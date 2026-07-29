# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **Data Project Starter Kit**, a public template repository for
bootstrapping Python data engineering/science/analytics projects (ETL, ML
pipelines, APIs, dashboards) with good practices already wired in:
reproducible environment, modular code, tests, lint/format standards, docs
generated from docstrings, pre-commit hooks, and CI.

The template was built from `docs/guia-boas-praticas.md` (Portuguese) —
that page explains the *why* behind every convention below, with links to
each tool's official docs. The user-facing quickstart lives in `README.md`;
this file is about how an agent should operate in this specific repo.

`app/pipeline/{extract,transform,load}.py` are intentionally generic
placeholders (`raise NotImplementedError` + TODO comments) — this repo is
the template itself, not a finished pipeline. Don't "complete" them
speculatively; they get implemented when someone uses this template for a
real project.

## Commands

```bash
uv sync                  # install everything from uv.lock
uv run task format       # ruff check --fix . && ruff format .
uv run task lint         # ruff check . && ruff format --check .
uv run task test         # pytest -v
uv run task docs         # mkdocs serve (local docs site)
uv run mkdocs build --strict   # verify docs build cleanly (used instead of serve in CI-like checks)
uv run pre-commit run --all-files
```

Single test: `uv run pytest tests/test_transform.py -k test_name`.

There is no `uv run python app/main.py` smoke test that will pass yet —
`main.py` calls the placeholder pipeline functions, which raise
`NotImplementedError` by design until a concrete project fills them in.

## Architecture

```
app/
├── main.py            # orchestrates extract -> transform -> load, __main__ guard
└── pipeline/
    ├── extract.py     # placeholder: signature + Google docstring + TODO
    ├── transform.py
    └── load.py
tests/                 # one test file per pipeline module, AAA-style,
                        # each currently a pytest.skip("TODO: ...") stub
docs/                   # MkDocs Material site; pipeline.md pulls docs
                        # straight from the app/pipeline docstrings via
                        # mkdocstrings — keep docstrings accurate, don't
                        # hand-write duplicate API docs.
                        # guia-boas-praticas.md is the full uv/Ruff-focused
                        # practices guide (source of truth for "why");
                        # ia-como-acelerador.md is Claude Code prompts.
data/input/, data/output/   # gitignored except .gitkeep; example I/O only
```

`app/`, `app/pipeline/`, and `tests/` all have `__init__.py` and the project
runs with `[tool.uv] package = false` in `pyproject.toml` — the project is
never installed as a wheel, `app` is imported as a plain top-level package
via pytest's rootdir insertion. Don't add a `[build-system]`/hatchling
section back in without a reason; it previously broke `uv sync` because it
required a `README.md`-referencing build step this template doesn't need.

Ruff is configured with `select = ["E","F","I","D","UP","B","S"]` and
Google-style docstring convention; `tests/*` is exempted from `D` and `S101`
(docstrings and `assert` usage) via `[tool.ruff.lint.per-file-ignores]`.

`mkdocs.yml` uses a `!!python/name:` tag for the Mermaid superfences
formatter, which the pre-commit `check-yaml` hook's safe loader can't
parse — that file is deliberately excluded from that hook
(`.pre-commit-config.yaml`), not a bug to "fix".

## Critical rules (carried over from the source guide)

- **Never use `git commit --no-verify`.** If pre-commit or CI fails, fix
  what it flags — AI agents reach for this bypass more readily than humans
  do, and it defeats the whole point of the hooks.
- **Every bug fix gets a new regression test** (pytest, Arrange-Act-Assert).
- **Prefer small, atomic commits/PRs** — one concern per commit, on the
  incremental-adoption order the guide lays out (environment → code →
  tests → lint/tasks → docs → hooks/CI), not one giant "fix everything"
  change.
- When extending this template for a real project, keep the placeholder
  pattern in mind: replace one `TODO` at a time and un-skip its matching
  test in the same change, rather than rewriting the whole pipeline at
  once.

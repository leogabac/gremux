# AGENTS

## Purpose

`gremux` is a small Python CLI for launching `tmux` sessions from declarative YAML.
The repo is early-stage and compact, so agents should optimize for small, coherent changes that preserve current behavior.

## Repo Map

- `src/gremux/cli.py`: main CLI entrypoint built with `argparse`. Dispatches to `config`, `places`, or the default interactive sessionizer flow.
- `src/gremux/cmds/`: thin command handlers.
  - `config.py`: `config up`, `config show`, `config create`.
  - `places.py`: creates or updates `~/.config/gremux/places.yaml`.
  - `sessionizer.py`: interactive project picker using `fzf`, then launches/attaches a tmux session.
- `src/gremux/struct/`: actual domain model and orchestration.
  - `parser.py`: resolves local `grem.yaml`, then falls back to `~/.config/gremux/default.yaml`, then an in-memory default.
  - `grem.py`: `Grem` session object and `launch()` logic.
  - `context.py`: enums plus `Pane` and `Window`; `Window.apply()` is where pane splitting, directory changes, and command dispatch happen.
  - `logger.py`: colored stdout logger.
- `templates/`: example `grem.yaml` files.
- `test/README.md`: roadmap only. There is no automated test suite in the repo right now.
- `pyproject.toml`: package metadata and console scripts.
- `PKGBUILD`: Arch packaging metadata.

## Architecture

The runtime flow is:

1. `gremux.cli:main()` parses args.
2. A command module decides what source path to use.
3. `gremux.struct.Parser` loads YAML and converts it into a `Grem` object.
4. `Grem.launch()` creates or reuses a tmux session through `libtmux`.
5. Each `Window` applies its layout, creates splits, `cd`s panes into the target directory, and sends pane commands.

The important split is:

- `cmds/*` should stay thin and mostly coordinate I/O and CLI behavior.
- `struct/*` owns parsing, defaults, and tmux session behavior.

If a change affects how sessions are built or applied, it probably belongs in `struct/`, not in the CLI layer.

## Runtime Assumptions

- Python `>=3.9`
- `libtmux`
- `PyYAML`
- `tmux` installed and running/available
- `fzf` for the default sessionizer flow
- `zoxide` only if using `gremux places create --source zoxide`

The code writes user config under `~/.config/gremux/`:

- `places.yaml`
- `places.bak`
- `default.yaml`

Be careful with changes that touch these paths; they affect the real user environment, not just the repo.

## Current Behavior And Constraints

- No local `grem.yaml`:
  - parser falls back to `~/.config/gremux/default.yaml`
  - if that also does not exist, parser builds a one-window in-memory default
- Existing tmux session with the target session name:
  - current behavior is to attach to it instead of recreating it
- `config show` currently prints the source YAML file directly; it does not show the fully resolved in-memory config
- `Window.apply()` currently:
  - applies layout
  - creates pane splits
  - sends `cd` commands
  - sends each configured command
  - clears the pane afterwards
- Some data model fields are present but not yet wired through:
  - `Pane.focus`
  - `Pane.env`
- README and roadmap indicate several planned features are not implemented yet. Do not infer support that the code does not currently have.

## Change Guidance

- Preserve the thin CLI / rich struct split.
- Prefer extending the parser and dataclasses before adding ad hoc dict logic in command modules.
- Keep YAML compatibility in mind. Templates and README examples use:
  - `session.name`
  - `session.windows[]`
  - `window.name`
  - `window.layout`
  - `window.panes[]`
  - `pane.cwd`
  - `pane.command`
- The parser currently assumes panes contain both `cwd` and `command`. If you loosen schema requirements, update parsing carefully.
- If you change config semantics, update:
  - `README.md`
  - relevant files in `templates/`
  - roadmap notes in `test/README.md` if the work closes or changes planned items
- Keep terminal-facing behavior simple. This is a CLI that shells out to external tools; avoid adding heavy framework complexity.

## Validation Strategy

There is no automated test suite yet, so validation is mostly targeted manual checking.

Useful commands:

```bash
python -m compileall src
python -m gremux.cli --version
python -m gremux.cli config show --source templates/demo.yaml
python -m gremux.cli config show --source templates/experiments.yaml
```

For tmux-affecting changes, validate with care because behavior depends on local tools and an interactive terminal session. Prefer checking parser behavior and non-interactive paths first if a full tmux session cannot be exercised.

## Agent Boundaries

When splitting work across agents, use these boundaries:

- CLI and argument UX:
  - `src/gremux/cli.py`
  - possibly `src/gremux/cmds/*`
- Config parsing and defaults:
  - `src/gremux/struct/parser.py`
  - `src/gremux/struct/context.py`
  - `src/gremux/struct/grem.py`
- User config file management:
  - `src/gremux/cmds/places.py`
  - `src/gremux/cmds/config.py`
- Docs and examples:
  - `README.md`
  - `templates/*`
  - `test/README.md`
  - `PKGBUILD` if release metadata changes

Avoid having multiple agents edit the same layer at once unless the change is trivial.

## Known Rough Edges

- `README.md`, CLI version strings, and `pyproject.toml` version metadata are not perfectly aligned.
- `config create` only supports `--source default`.
- `config show` is a raw file dump, not a resolved config view.
- Paths under `~/.config/gremux/` are written directly without explicit directory creation in the command handlers.
- The roadmap explicitly calls out crash/clean-exit and config improvements as unfinished.

Agents should treat the current implementation as functional-but-early, and prefer incremental improvements over broad refactors unless asked otherwise.

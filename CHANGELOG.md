# Changelog

## Unreleased

### Changed

- default windows are now named `main` instead of `0`

### Added

- `gremux config create --source session` to export the current tmux session's
  windows and pane directories into a project `grem.yaml`
- session export metadata for active windows/panes, pane titles, and active
  programs, plus `--dry-run` and `--include-start-commands` export options
- `gremux config diff-session` to compare the live session with `grem.yaml`
- `gremux config update-session` to merge live pane/window structure while
  retaining configured pane commands
- `gremux config sync --replace` to recreate an existing session from YAML

### Fixed

- window layouts are applied after panes are created, so configured horizontal,
  vertical, and main layouts take effect
- `layout: null` no longer creates implicit tmux splits
- session export now assigns layouts to multi-pane windows so their panes are
  recreated on launch

## [0.1.3] - 2026-04-28

### Added

- `gremux attach` interactive tmux session picker using `questionary`
- `gremux attach --last` for tmux-native attach behavior
- `gremux config use NAME` to copy a saved template into the current project
- `gremux config use --interactive` to pick a saved template interactively
- `gremux config save NAME` to save the current project config as a template
- `gremux config list` to list saved templates
- `gremux config edit` to open `~/.config/gremux/` in the editor defined by `$EDITOR`
- template import/export support under `~/.config/gremux/templates/`

### Changed

- `config show` now prints the resolved configuration instead of dumping the raw source file
- template import rewrites `session.name` to the current directory name
- template save rewrites `session.name` to the template name
- `gremux` and `gremux config up` now share the same launch path through `Grem.launch()`

### Fixed

- parser handling for templates that omit `cwd`
- parser handling for pane commands stored as a string or a list
- creation of `~/.config/gremux/` before writing global config files
- clearer error handling for missing `tmux`, `fzf`, `zoxide`, and malformed places config
- README and roadmap drift around the current command set

## [0.1.2] - 2026-04-28

### Notes

- This tag existed only as an intermediate development state while the release work was underway.
- The current repository state is tracked in `0.1.3`.

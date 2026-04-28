# Roadmap

This file tracks the next visible feature work for `gremux`.
It is intentionally short and release-oriented so it stays aligned with the current code.

## Release 0.1.3

- [x] Declarative YAML tmux session management
- [x] Interactive project sessionizer
- [x] Resolve `grem.yaml` with fallback to `~/.config/gremux/default.yaml`
- [x] Show resolved configuration with `config show`
- [x] Create the default global config safely
- [x] Save templates into `~/.config/gremux/templates/`
- [x] Load templates back into a project with name rewriting
- [x] List saved templates
- [x] Open the config directory in the editor
- [x] Interactive attach picker for active tmux sessions
- [x] `gremux attach --last` for tmux-native attach behavior

## Next Features

- [ ] `config validate` to check a local `grem.yaml` without launching tmux
- [ ] `config doctor` to check required tools and config locations
- [ ] `config create --source session` to build a starter config from a running tmux session
- [ ] `attach --session NAME` as a non-interactive attach shortcut
- [ ] support absolute pane paths in addition to project-relative `cwd`
- [ ] implement `Pane.env`
- [ ] implement `Pane.focus`
- [ ] add a `--dry-run` mode for `config up`
- [ ] add optional session replacement behavior for existing sessions

## Longer-Term Ideas

- [ ] add template tags or categories under `~/.config/gremux/templates/`
- [ ] add a template picker for `config use` when the archive gets larger
- [ ] add `places list` and `places edit`
- [ ] add `config remove NAME` for deleting saved templates safely
- [ ] build a TUI to manage configuration files

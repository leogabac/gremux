# gremux

![Static Badge](https://img.shields.io/badge/repo-gremux-blue?logo=github) ![Static Badge](https://img.shields.io/badge/status-dev-red?logo=github)

A declarative [tmux](https://github.com/tmux/tmux) session manager.

> [!NOTE]
> This project is _very_ early in development. Only a few features are implemented, and there is a long roadmap to cover.
> If you have any feature requests, leave an _issue_.

gremux automates the process of launching a `tmux` session exactly how you want it in a _declarative_ way. That is, given a static configuration file `grem.yaml`, `gremux` will parse it and attach you to a session that matches that setup.

This project started when I got tired of having to manually set up my `tmux` panes and windows each time I rebooted my laptop. Thus, I can spend _many hours_ automating a process that takes literal seconds.

Here is a list of a few similar projects:
* [tmuxp](https://github.com/tmux-python/tmuxp): Session manager for tmux, build on libtmux.
* [tmuxinator](https://github.com/tmuxinator/tmuxinator): Manage complex tmux sessions easily
* [disconnected](https://github.com/austinwilcox/disconnected): Simple tmux session creator

**Why choose `gremux`?**

You don't have to if you don't want. That's the beauty of FOSS. This project was started as something to kill the time while waiting for my experiments during my PhD. I use it as my main tool, and it would be amazing if other people found it useful.

Additionally, I do projects in order to teach myself some design patterns to _eventually_ be a better programmer. I don't mind reinventing the wheel from time to time in order to learn something new.

> [!NOTE]
> The name _gremux_.
> I am obsessed with VTubers, and put references everywhere I can. This is a reference to [Gigi Murin](https://www.youtube.com/@holoen_gigimurin), whose fanbase are called _grems_.

## Features

* Declarative YAML tmux session configuration in a per-project basis
* `tmux-sessionizer`, inspired by [ThePrimeagen's](https://github.com/ThePrimeagen/tmux-sessionizer) script.

For a list of TODOs, see the [roadmap](./test/README.md)

## Installation

This project is in very early stages of development, there is no proper way for installation other than a local python package.

1. Create a (global) virtual environment where your shell defaults into.
2. Install the repository with `pip`

```sh 
pip install gremux
```
3. Install `fzf` from your package manager.

Run `gremux` to open the sessionizer.

## Setup

### Common places

You must create the (global config) file `~/.config/gremux/places.yaml`. To create it, run
```sh
gremux places create --source default
```
This will create a basic `places.yaml` with your home directory. To add more places, you can manually edit the file or run
```sh
gremux places create --add dir1 dir2 dir3
```

> [!TIP]
> If you use `zoxide`, then you can choose to use the database as a source
> ``` sh
> gremux places create --source zoxide
> ```
> And optionally you can add the `--maximum N` flag to only add the first $N$ elements from the database.

Here is an example of how it should look like.
```yaml
places:
  - "~"
  - "~/Documents/"
  - "~/Documents/mnt/"
  - "~/Documents/phd/"
  - "~/Documents/projects/"
```
which is intended to be the list of the common places you visit in your system. This information is used by the _sessionizer_ to know where to look

### Configuration file

tmux sessions are launched by parsing a configuration file called `grem.yaml` that is intended to be placed on your project's root. If no file is found, it will default to a single window-pane setup.

See the [templates](./templates/) directory for some examples. Here are a few notes of the keywords

**session**
- `name`: the name of the session
- `windows`: list of windows to open


**windows**
- `name`: the name of the window
- `layout`: layout to use. Must match [tmux window layouts](https://github.com/tmux/tmux/wiki/Getting-Started#window-layouts) or `null` to do nothing.
- `panes`: list of panes to split

**panes**
- `cwd`: Working directory for the pane. Assumed to be **relative** to the project's root.
- `command`: list of commands to execute in the current pane. They are executed sequentially.

## Usage

There are two basic ways to launch a session

1. Run `gremux`, type your project's directory and hit `<enter>`. This will use the project's `grem.yaml` if available, otherwise, it will default to a generic one window/panel default.
2. If you are alredy somewhere, run
```sh
gremux config up --source /path/to/grem.yaml
```
if no `--source` is provided, it defaults to `pwd`

**Other useful commands**

* To see the configuration that is going to be used, run
```sh
gremux config show
```
* To create the default configuration under `~/.config/gremux/default.yaml`
```sh
gremux config create --source default
```



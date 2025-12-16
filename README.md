# gremux

Another tmux session manager.

I got tired of having to manually set up my `tmux` panes and windows each time I rebooted my laptop. Thus, I can spend _many hours_ automating a process that takes literal seconds.

There is a perfectly fine project called [tmuxp](https://github.com/tmux-python/tmuxp) that does exactly what this project wishes to eventually accomplish. However, as a good engineer, I felt the urge to reinvent the wheel out of boredom, and now I am too invested to quit.

Additionally, I do projects in order to teach myself some design patterns to _eventually_ be a better programmer and **NOT** code like a physicist.

> [!NOTE]
> The name _gremux_.
> I am obsessed with VTubers, and put references everywhere I can. This is a reference to [Gigi Murin](https://www.youtube.com/@holoen_gigimurin).

## Installation

As this project is very early in development, there is no proper way for installation other than a local python package.

1. Create a (global) virtual environment, where your shell defaults into, e.g.
2. Install the repo with `pip`

```sh 
pip install git+https://github.com/leogabac/gremux.git
```
3. Install `fzf` from your package manager.

Run `gremux` to oppen the sessionizer.

## Setup

### Default `sessionizer`

Inspired by [tmux-sessionizer](https://github.com/ThePrimeagen/tmux-sessionizer) by The Primeagen.

* Create a `places.yml` under `~/.config/gremux/places.yml` with a list of your common places
```
places:
  - "~"
  - "~/Documents/"
  - "~/Documents/projects/"
```

If no `grem.yaml` is found in the project's root, it will default to a basic setup.

### `grem.yaml` file

The `grem.yaml` file lets you write a static setup for your project. On your project's root write something similar to

```
session:
  name: experiments

  windows:
    # ide
    - name: ide
      layout: null
      panes:
        - cwd: .
          command:
            - source ./.venv/bin/activate.fish
            - nvim

    # running stuff and data
    - name: run
      layout: main-horizontal
      panes:
        # running
        - cwd: .
          command:
            - source .venv/bin/activate.fish
        # data
        - cwd: ./data
          command:
            - source .venv/bin/activate.fish

    # jupyter server
    - name: jupyter
      layout: null
      panes:
        - cwd: .
          command:
            - source .venv/bin/activate.fish
            - cd $HOME
            - jupyter lab --no-browser --port=8001

```

> [!NOTE]
> `cwd` is relative to project's root.

## Features to implement (WIP)

Here is a basic roadmap of my intentions with this project:

* Have a `default.yaml` under the config dir to drop into
* `up` a session from a config file
* `show` config file well formated
* `load` the config file to my current attached session
* `create` config file from session name
* `archive save` config files into templates directory
* `archive set` bring a local grem file from something in the archive
* Build a TUI to manage your configuration files

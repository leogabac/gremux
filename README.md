# gremux: A static tmux session manager

I got tired of having to manually set up my `tmux` panes and windows each time I rebooted my laptop. Thus, I can spend _many hours_ automating a process that takes literal seconds.

There is a perfectly fine project called [tmuxp](https://github.com/tmux-python/tmuxp) that does exactly what this project wishes to eventually accomplish. However, as a good engineer, I felt the urge to reinvent the wheel out of boredom, and now I am too invested to quit.

Additionally, I do projects in order to teach myself some design patterns to _eventually_ be a better programmer and **NOT** code like a physicist.

> [!NOTE]
> The name _gremux_.
> I am obsessed with VTubers, and put references everywhere I can. This is a reference to [Gigi Murin](https://www.youtube.com/@holoen_gigimurin).

## Features to implement (WIP)

Here is a basic roadmap of my intentions with this project:

* Choose a markup language (YAML most probably) and design the API
* Parse a `grem.yaml` file with configurations
* Use [`libtmux`](https://github.com/tmux-python/libtmux) to manage tmux based on config file
* Allow for global settings
* Build a TUI to manage your configuration files
* Allow to "dump" the state of a tmux session into a perfectly formatted configuration file

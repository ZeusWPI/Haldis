# HLDS support in Vim

Add syntax highlighting for HLDS, the Haldis Language for Describing Servings, to your editor!

## Installation

Install these files as

* `ftdetect/hlds.vim`
* `ftplugin/hlds.vim`
* `syntax/hlds.vim`
* `indent/hlds.vim`

in your Vim runtime directory.

For example if you're using a *NIX such as Linux or macOS:
```sh
for kind in ftdetect ftplugin syntax indent; do
	mkdir -p ~/.vim/$kind
	cp $PWD/$kind.vim ~/.vim/$kind/hlds.vim
done
```

If you use [Neovim](https://neovim.io/) instead of Vim:
```sh
for kind in ftdetect ftplugin syntax indent; do
	mkdir -p ~/.config/nvim/$kind
	cp $PWD/$kind.vim ~/.config/nvim/$kind/hlds.vim
done
```

If you want to use the latest version, you can create symlinks instead of copying by substituting
`ln -s` for `cp`.

Restart Vim to enable support for HLDS.

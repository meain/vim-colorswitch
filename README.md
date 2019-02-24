# `vim-colorswitch`

![gif](https://i.imgur.com/eH7LpKa.gif)


## Installation

> Install `colour` package from pypi using
```
pip3 install colour
``` 
and add it to your package manager (example for vim-plug)

```
if has('nvim')
  Plug 'meain/vim-colorswitch', { 'do': 'UpdateRemotePlugins' }
else
  Plug 'meain/vim-colorswitch'
  Plug 'roxma/nvim-yarp'
  Plug 'roxma/vim-hug-neovim-rpc'
endif
```


## Usage


Exposes one command

```
:ColorSwap
```

You can call it on any line with a color value and it will cycle through `hex`, `rgb`, 'rgba', 'hsl' values for that
color and replace the value in the line.

You could maybe create a remap like:
```

nnoremap <leader>c :exec ColorSwap()<CR>
```

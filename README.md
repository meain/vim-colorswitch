# `vim-colorswitch`

## Installation

> Install `colour` package from pypi using
```
pip3 install colour
``` 
and add it to your package manager
```
Plug 'meain/vim-colorswitch', { 'do': 'UpdateRemotePlugins' }
```


## Usage

Exposes one command

```
:ColorSwap
```

You can call it on any line with a color value and it will cycle through `hex`, `rgb`, 'rgba', 'hsl' values for that
color and replace the value in the line.

# emacs stuff in vim
This plugin adds some emacs functions to vim. Done in python.

### delete word `<M-d>`

Delete chars till the word and, if word was really close, delete the word too. It
respects camel-case and `"_"` notation. For example, `MyFuncWithArgs` is treated
as 4 words, so is `my_func_with_arg`.

### change word case `<M-u>`, `<M-l>`, `<M-c>`

Find a word, change case - upper, lower or capitalized - and move to the end of the word

### movements `<M-Left>`, `<M-Right>`
Move to the start or end of the word. It respects camel-case and `"_"` notation.

### run command `<M-x>`
Enter command prompt, same as pressing `:`. Works in all modes.

## Installation
For Plug plugin manager, add this line after `plug#begin()` in `.vimrc`
```
Plug 'aanatoly/vim-emacs-keys'
```


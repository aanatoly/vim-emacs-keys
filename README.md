# emacs stuff in vim
This plugin adds some emacs functions to vim. Done in python.

**kill-word** `<M-d>`

Delete chars till the word and, if word was really close, delete the word too. It
has few extras
 * camel-case notation. Deletion stop before next block. For example,
   string `MyFuncWithArgs` is treated as 4 words
 * words with `_`. String `my_func_with_arg` is 4 words too.


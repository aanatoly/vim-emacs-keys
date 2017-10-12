" Emacs keys bindings and functions
" Last Change:  2017 Oct 4
" Maintainer:   Anatoly Asviyan <aanatoly@gmail.com>
" Licence:      GPLv2

if exists("g:loaded_emacs_keys") || &cp || &modifiable == 0
  finish
endif
let g:loaded_emacs_keys = 100


let s:emacs_py = resolve(expand('<sfile>:p:h')) ."/main.py"
execute 'pyfile ' . s:emacs_py

function! KillWordNormal()
    py kill_word_normal()
endfunc
function! KillWordInsert()
    py kill_word_insert()
endfunc

command! KillWordNormalCmd call KillWordNormal()
nnoremap <A-d> :KillWordNormalCmd<CR>
command! KillWordInsertCmd call KillWordInsert()
inoremap <A-d> <C-o>:KillWordInsertCmd<CR>

" Emacs keys bindings and functions
" Last Change:  2017 Oct 4
" Maintainer:   Anatoly Asviyan <aanatoly@gmail.com>
" Licence:      GPLv2

if !has('python')
	finish
endif

if exists("g:emacs_keys_loaded") || &cp || &modifiable == 0
  finish
endif
let g:emacs_keys_loaded = 100


let g:InsCol = 0
let g:InsRow = 0
autocmd InsertEnter * let g:InsCol = col('.') |
	\ let g:InsRow = line('.')
autocmd CursorMovedI * let g:InsCol = col('.') |
	\ let g:InsRow = line('.')

let s:emacs_py = resolve(expand('<sfile>:p:h')) ."/main.py"
execute 'pyfile ' . s:emacs_py

function! KillWord(mode)
    py kill_word()
endfunc
nnoremap <A-d> :call KillWord("n")<CR>
inoremap <A-d> <C-o>:call KillWord("i")<CR>

function! ChangeWordCase(mode, conv)
    py change_word_case()
endfunc
nnoremap <A-u> :call ChangeWordCase("n", "u")<CR>
inoremap <A-u> <C-o>:call ChangeWordCase("i", "u")<CR>
nnoremap <A-l> :call ChangeWordCase("n", "l")<CR>
inoremap <A-l> <C-o>:call ChangeWordCase("i", "l")<CR>
nnoremap <A-c> :call ChangeWordCase("n", "c")<CR>
inoremap <A-c> <C-o>:call ChangeWordCase("i", "c")<CR>


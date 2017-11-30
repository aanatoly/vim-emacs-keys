" Emacs keys bindings and functions
" Last Change:  2017 Oct 4
" Maintainer:   Anatoly Asviyan <aanatoly@gmail.com>
" Licence:      GPLv2

if exists("g:emacs_keys_loaded") || &cp || &modifiable == 0
  finish
endif
let g:emacs_keys_loaded = 1

if has("python3")
  let s:pyfile = "py3file "
  let s:py = "py3 "
elseif has("python")
  let s:pyfile = "pyfile "
  let s:py = "py "
else
  echohl Error
  echo "Error: emacs-keys requires vim compiled with +python or +python3"
  echohl None
  finish
endif

let s:main_py = resolve(expand('<sfile>:p:h')) ."/main.py"
execute s:pyfile . s:main_py


let g:InsCol = 0
let g:InsRow = 0
autocmd InsertEnter * let g:InsCol = col('.') |
  \ let g:InsRow = line('.')
autocmd CursorMovedI * let g:InsCol = col('.') |
  \ let g:InsRow = line('.')

let s:emacs_py = resolve(expand('<sfile>:p:h')) ."/main.py"
execute s:pyfile . s:emacs_py


function! KillWord(mode)
    exec s:py 'kill_word()'
endfunc
nnoremap <A-d> :call KillWord("n")<CR>
inoremap <A-d> <C-o>:call KillWord("i")<CR>

function! ChangeWordCase(mode, conv)
    exec s:py 'change_word_case()'
endfunc
nnoremap <A-u> :call ChangeWordCase("n", "u")<CR>
inoremap <A-u> <C-o>:call ChangeWordCase("i", "u")<CR>
nnoremap <A-l> :call ChangeWordCase("n", "l")<CR>
inoremap <A-l> <C-o>:call ChangeWordCase("i", "l")<CR>
nnoremap <A-c> :call ChangeWordCase("n", "c")<CR>
inoremap <A-c> <C-o>:call ChangeWordCase("i", "c")<CR>

function! FindWord(mode, dir)
    exec s:py 'find_word()'
endfunc
nnoremap <A-Right> :call FindWord("n", "r")<CR>
inoremap <A-Right> <C-o>:call FindWord("i", "r")<CR>
nnoremap <A-Left> :call FindWord("n", "l")<CR>
inoremap <A-Left> <C-o>:call FindWord("i", "l")<CR>

nnoremap <A-x> :
vnoremap <A-x> :
inoremap <A-x> <C-o>:

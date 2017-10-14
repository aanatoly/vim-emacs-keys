
import vim
import string

################################################
# {{{ misc functions

debug = bool(int(vim.eval('exists("g:emacs_keys_debug")')))

def dbg_init(title):
    if not debug:
        return
    buf = vim.current.buffer
    buf[0] = title + ": "

def dbg_add(msg):
    if not debug:
        return
    buf = vim.current.buffer
    buf[0] += msg + "; "


is_not_alnum = lambda x: not str.isalnum(x)
is_alnum = lambda x: str.isalnum(x)
is_upper = lambda x: str.isupper(x)
is_lower_or_digit = lambda x: str.isdigit(x) or str.islower(x)

def skip_chars(line, slen, pos, test):
    while pos < slen:
        if not test(line[pos]):
            break
        pos += 1
    return pos

def set_cursor(row, col):
    vim.current.window.cursor = row + 1, col
    dbg_add("set pos %s, %s" % (row, col))

def get_cursor(mode='n'):
    if mode == 'n':
        row, col = vim.current.window.cursor
        row -= 1
    elif mode == 'i':
        col = int(vim.eval("g:InsCol")) - 1
        row = int(vim.eval("g:InsRow")) - 1
    else:
        raise Exception("Unknown mode " + mode)
    return row, col

def get_text():
    return vim.current.line, len(vim.current.line)

def init(title):
    dbg_init("kill_word")
    mode = vim.eval("a:mode")
    buf = vim.current.buffer
    row, col = get_cursor(mode)
    dbg_add("mode %s; pos %s, %s" % (mode, row, col))
    return mode, buf, row, col

def search(pattern, flags):
    cmd = 'search("%s", "%s")' % (pattern, flags)
    rc = int(vim.eval(cmd))
    dbg_add("search %s" % rc)
    row, col = get_cursor()
    dbg_add("pos %s, %s" % (row, col))
    return rc, row, col


# }}}

################################################
# {{{ word manipulation

CLOSE_RANGE = 3

def kill_word():
    mode, buf, orow, ocol = init("kill_word")

    rc, row, col = search("[a-zA-Z0-9]", "Wc")
    if rc == 0:
        # no words found - delete till the end of a file
        buf[orow] = buf[orow][:ocol]
        del buf[orow+1:]
        set_cursor(orow, ocol)
        return

    line, slen = get_text()
    # if word is close - include it in the range
    if row == orow and (col - ocol < CLOSE_RANGE):
        col = skip_chars(line, slen, col, is_upper)
        col = skip_chars(line, slen, col, is_lower_or_digit)

    # delete the range
    buf[orow] = buf[orow][:ocol] + buf[row][col:]
    del buf[orow+1:row+1]

    set_cursor(orow, ocol)

conv = {
    'l': string.lower,
    'u': string.upper,
    'c': string.capitalize
}

def change_word_case():
    mode, buf, orow, ocol = init("change_word_case")

    rc, row, col = search("[a-zA-Z0-9]", "Wc")
    if rc == 0:
        return

    line, slen = get_text()
    ecol = skip_chars(line, slen, col, is_alnum)
    func = conv[vim.eval("a:conv")]
    buf[row] = line[:col] + func(line[col:ecol]) + line[ecol:]
    set_cursor(row, ecol)

# }}}

################################################
# {{{ movements

def find_word_end():
    mode, buf, orow, ocol = init("find_word_end")

# }}}


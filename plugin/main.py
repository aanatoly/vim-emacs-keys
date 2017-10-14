
import vim
import string

def skip_chars(line, slen, pos, test):
    while pos < slen:
        if not test(line[pos]):
            break
        pos += 1
    return pos

def set_cursor(row, col):
    vim.current.window.cursor = row + 1, col

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

is_not_alnum = lambda x: not str.isalnum(x)
is_alnum = lambda x: str.isalnum(x)
is_upper = lambda x: str.isupper(x)
is_lower_or_digit = lambda x: str.isdigit(x) or str.islower(x)

################################################
# {{{ kill word


def kill_alg_2(line, slen, pos):
    # find word
    anpos = skip_chars(line, slen, pos, is_not_alnum)

    # if no word - delete rest of the line
    if anpos == slen:
        return slen - 1

    # if gap is small, delete both gap and a word
    gap = anpos - pos
    if '\t' in line[pos:anpos]:
        gap += 4
    if gap < 4:
        anpos = skip_chars(line, slen, anpos, is_upper)
        return skip_chars(line, slen, anpos, is_lower_or_digit)

    # otherwise delete the gap and bring word forward
    return anpos


def kill_word():
    mode = vim.eval("a:mode")
    buf = vim.current.buffer
    line, slen = get_text()
    row, col = get_cursor(mode)

    # delete empty lines
    if slen == 0:
        while row < len(buf):
            if len(buf[row]):
                break
            del buf[row]
        return

    # insert mode, end of line - join next line
    if col == slen:
        vim.command('/\w')
        erow, ecol = get_cursor()
        # if no word found - delete till the end of a buffer
        if erow < 1:
            del buf[row + 1:]
            set_cursor(row, col)
            return
        # otherwise delete till the word
        buf[row] += buf[erow][ecol:]
        del buf[row + 1:erow + 1]
        set_cursor(row, col)
    elif col == slen -1:
        buf[row] = line[:col]
    else:
        pos = kill_alg_2(line, slen, col)
        buf[row] = line[:col] + line[pos:]
    slen = len(buf[row])
# }}}

################################################
# {{{ chage word case

conv = {
    'l': string.lower,
    'u': string.upper,
    'c': string.capitalize
}

# FIXME: Can't make vim command "/\w' do right thing. So write it myself
def find_word(mode, buf, row, col):
    while row < len(buf):
        line = buf[row]
        slen = len(line)
        while col < slen:
            if line[col].isalnum():
                return (row, col)
            col += 1
        col = 0
        row += 1

    return (None, None)


def change_word_case():
    mode = vim.eval("a:mode")
    buf = vim.current.buffer

    row, col = find_word(mode, buf, *get_cursor(mode))
    if row is None:
        return
    line = buf[row]
    slen = len(line)
    ecol = skip_chars(line, slen, col, is_alnum)
    func = conv[vim.eval("a:conv")]
    buf[row] = line[:col] + func(line[col:ecol]) + line[ecol:]
    set_cursor(row, ecol)
# }}}

################################################
# {{{ cursor movements

def find_word_end():
    pass
# }}}



import vim


def skip_chars(line, slen, pos, test):
    while pos < slen:
        if not test(line[pos]):
            break
        pos += 1
    return pos

################################################
# {{{ kill word
def kill_alg_1(line, slen, pos):
    if line[pos:pos+2].isspace():
        pos = skip_chars(line, slen, pos, lambda x: str.isspace(x))
    else:
        if line[pos].isspace():
            pos += 1
        if line[pos].isalnum():
            pos = skip_chars(line, slen, pos, lambda x: str.isalnum(x))
        else:
            pos = skip_chars(line, slen, pos, lambda x: str.isspace(x) or not str.isalnum(x))
    return pos


def kill_alg_2(line, slen, pos):
    # find word
    test = lambda x: not str.isalnum(x)
    anpos = skip_chars(line, slen, pos, test)

    # if no word - delete rest of the line
    if anpos == slen:
        return slen - 1

    # if gap is small, delete both gap and a word
    gap = anpos - pos
    if '\t' in line[pos:anpos]:
        gap += 4
    if gap < 4:
        test = lambda x: str.isupper(x)
        anpos = skip_chars(line, slen, anpos, test)
        test = lambda x: str.isdigit(x) or str.islower(x)
        return skip_chars(line, slen, anpos, test)

    # otherwise delete the gap and bring word forward
    return anpos


def kill_word():
    mode = vim.eval("a:arg")
    cw = vim.current.window
    cb = vim.current.buffer
    if mode == 'n':
        row, col = cw.cursor
        row -= 1
    else:
        col = int(vim.eval("g:InsCol")) - 1
        row = int(vim.eval("g:InsRow")) - 1
    line = cb[row]
    slen = len(cb[row])

    # delete empty lines
    if slen == 0:
        while row < len(cb):
            if len(cb[row]):
                break
            del cb[row]
        return

    # insert mode, end of line - join next line
    if col == slen:
        vim.command('/\w')
        erow, ecol = cw.cursor
        erow -= 1
        # if no word found - delete till the end of a buffer
        if erow < 1:
            del cb[row + 1:]
            cw.cursor = (row + 1, col)
            return
        # otherwise delete till the word
        cb[row] += cb[erow][ecol:]
        del cb[row + 1:erow + 1]
        cw.cursor = (row + 1, col)
    elif col == slen -1:
        cb[row] = line[:col]
    else:
        pos = kill_alg_2(line, slen, col)
        cb[row] = line[:col] + line[pos:]
    slen = len(cb[row])
# }}}


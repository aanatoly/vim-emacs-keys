
import vim

def kill_word_normal():
    kill_word("n")


def kill_word_insert():
    kill_word("i")

def skip_chars(line, slen, pos, test):
    while pos < slen:
        if not test(line[pos]):
            break
        pos += 1
    return pos


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
    # find first alnum
    test = lambda x: not str.isalnum(x)
    anpos = skip_chars(line, slen, pos, test)

    # if no alnum - delete rest of the line
    if anpos == slen:
        return slen - 1

    # if gap is small, delete the word along with the gap
    gap = anpos - pos
    print ":%s:" % line[pos:anpos]
    if '\t' in line[pos:anpos]:
        gap += 4
    if gap < 4:
        test = lambda x: str.isalnum(x)
        return skip_chars(line, slen, anpos, test)

    # otherwise delete the gap and bring word forward
    return anpos


def kill_word(mode):
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
    if slen == 0:
        while row < len(cb):
            if len(cb[row]):
                break
            del cb[row]
        return
    if col == slen -1:
        cb[row] = line[:col-1]
    else:
        pos = kill_alg_2(line, slen, col)
        cb[row] = line[:col] + line[pos:]
    slen = len(cb[row])
    # cb[0] = "mode %s, len %d, row %d, col %d" % (mode, slen, row, col)

# -*- coding: utf-8 -*-


__all__ = [
    'Caret',
    'StrList'
]

class Caret(object):

    # text nav operations
    MOVPREVCHAR = 1
    MOVNEXTCHAR = 2
    MOVPREVLINE = 3
    MOVNEXTLINE = 4
    MOVPREVWORD = 5
    MOVNEXTWORD = 6
    MOVTEXTHOME = 7
    MOVTEXTEND  = 8
    MOVLINEHOME = 9
    MOVLINEEND  = 10
    MOVPAGEUP   = 11
    MOVPAGEDOWN = 12

    # text selection operations
    SELPREVCHAR = 1
    SELNEXTCHAR = 2
    SELPREVLINE = 3
    SELNEXTLINE = 4
    SELPREVWORD = 5
    SELNEXTWORD = 6
    SELTEXTHOME = 7
    SELTEXTEND  = 8
    SELLINEHOME = 9
    SELLINEEND  = 10
    SELPAGEUP   = 11
    SELPAGEDOWN = 12
    SELCANCEL   = 13

    # text modification operations
    MODINSERTCHAR    = 1
    MODREPLACECHAR   = 2
    MODINSERTWORD    = 3
    MODINSERTLINE    = 4
    MODERASECHAR     = 5
    MODERASEWORD     = 6
    MODERASELINE     = 7
    MODDELETECHAR    = 8
    MODDELETEWORD    = 9
    MODDELETELINE    = 10
    MODINSERTNEWLINE = 11
    MODINSERTTAB     = 12
    MODDELSELECTION  = 13
    MODMOVESELECTION = 14

    # option flags
    AUTOINDENT = 1
    DEDENTONBKSPC = 2
    WHITESPACEHOME = 4

    __slots__ = ('line', 'column', 'indent', 'memcol', 'options',
                 'sline', 'scolumn', 'selecting', 'page_size')

    def __init__(self, indent=4, flags=AUTOINDENT|DEDENTONBKSPC):
        self._line = 0
        self._column = 0
        self.memcol = 0
        self.indent = indent
        self.options = flags
        self.sline = 0
        self.scolumn = 0
        self.selecting = False
        self._page_size = [80, 20]
        self._page_pos = [0, 0]

    def memorize(self):
        self.memcol = self.column

    def start_selection(self):
        if not self.selecting:
            self.sline = self.line
            self.scolumn = self.column
            self.selecting = True

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = max(0, int(value))
        if not (self.page_pos[1] <= self._line < self.page_pos[1] + self.page_size[1]):
            if self._line < self.page_pos[1]:
                self.page_pos[1] = self._line
            else:
                self.page_pos[1] = self._line - self.page_size[1]

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = max(0, int(value))
        if not (self.page_pos[0] <= self._column < self.page_pos[0] + self.page_size[0]):
            if self._column < self.page_pos[0]:
                self.page_pos[0] = self._column
            else:
                self.page_pos[0] = self._column - self.page_size[0]

    @property
    def page_size(self):
        return self._page_size[:]

    @page_size.setter
    def page_size(self, value):
        self._page_size[0] = int(value[0])
        self._page_size[1] = int(value[1])

    @property
    def page_pos(self):
        return self._page_pos[:]

    @page_pos.setter
    def page_pos(self, value):
        self._page_pos[0] = int(value[0])
        self._page_pos[1] = int(value[1])

    def page_scroll(self, hscroll, vscroll):
        self.page_pos[0] = max(0, self.page_pos[0] + hscroll)
        self.page_pos[1] = max(0, self.page_pos[1] + vscroll)


class StrList(object):

    """Represents a list of unicode strings."""

    __slots__ = ('lines', 'caret')

    def __init__(self):
        self.lines = []
        self.caret = Caret()

    def __len__(self):
        return len(self.lines)

    def __iter__(self):
        return iter(self.lines)

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        """StrList has strict use of setitem method.
        """
        if isinstance(key, int):
            if not isinstance(value, (str, unicode)):
                raise ValueError("str or unicode string expected.")
            self.items[key] = unicode(value)
        else:
            raise KeyError("int key expected.")

    def __delitem__(self):
        del self.lines[key]

    def __contains__(self, item):
        return item in self.lines

    @property
    def is_first_line(self):
        return self.caret.line == 0

    @property
    def is_last_line(self):
        return self.caret.line == len(self) - 1

    @property
    def current_line(self):
        ind = max(0, min(len(self.lines)-1, self.caret.line))
        return self.lines[ind]

    @property
    def current_length(self):
        return len(self.current_line)

    def get_indent_length(self, line_str):
        for i, ch in enumerate(line):
            if ch != ' ':
                return i

    def correct_column(self, line_index):
        self.caret.column = max(0, min(self.caret.memcol, len(self[line_index]))) 

    def mov_operation(self, op):
        # RIGHT
        if op == Caret.MOVNEXTCHAR:
            if self.caret.column < self.current_length:
                self.caret.column += 1
            elif not self.is_last_line:
                self.caret.line += 1
                self.caret.column = 0
            self.caret.memorize()

        # LEFT
        elif op == Caret.MOVPREVCHAR:
            if self.caret.column > 0:
                self.caret.column -= 1
            elif not self.is_first_line:
                self.caret.line -= 1
                self.caret.column = len(self[self.caret.line])
            self.caret.memorize()

        # UP
        elif op == Caret.MOVPREVLINE:
            if not self.is_first_line:
                self.caret.line -= 1
                self.correct_column(self.caret.line)

        # DOWN
        elif op == Caret.MOVNEXTLINE:
            if not self.is_last_line:
                self.caret.line += 1
                self.correct_column(self.caret.line)

        # CTRL+HOME
        elif op == Caret.MOVTEXTHOME:
            self.caret.line = 0
            self.caret.column = 0
            self.caret.memorize()

        # CTRL+END
        elif op == Caret.MOVTEXTEND:
            self.caret.line = len(self) - 1
            self.caret.column = len(self[self.caret.line])
            self.caret.memorize()

        # HOME
        elif op == Caret.MOVLINEHOME:
            self.caret.column = 0
            self.caret.memorize()

        # END
        elif op == Caret.MOVLINEEND:
            self.caret.column = len(self[self.caret.line])
            self.caret.memorize()

        # PAGEUP
        elif op == Caret.MOVPAGEUP:
            jump = self.caret.page_size[1] - 1
            self.caret.line -= jump
            self.correct_column(self.caret.line)

        # PAGEDOWN
        elif op == Caret.MOVPAGEDOWN:
            jump = self.caret.page_size[1] - 1
            self.caret.line = min(len(self) - 1, self.caret.line + jump)
            self.correct_column(self.caret.line)

        # CTRL+PAGEUP
        elif op == Caret.MOVPAGETOP:
            self.caret.line = self.caret.page_pos[1]
            self.correct_column(self.caret.line)

        # CTRL+PAGEDOWN
        elif op == Caret.MOVPAGEBOTOM:
            jump = (self.caret.page_pos[1] + self.caret.page_size[1]) - 1
            self.caret.line = min(len(self) - 1, jump)
            self.correct_column(self.caret.line)

    def sel_operation(self, op):
        # SHIFT+LEFT
        if op == Caret.SELPREVCHAR:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVPREVCHAR)

        # SHIFT+RIGHT
        elif op == Caret.SELNEXTCHAR:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVNEXTCHAR)

        # SHIFT+UP
        elif op == Caret.SELPREVLINE:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVPREVLINE)

        # SHIFT+DOWN
        elif op == Caret.SELNEXTLINE:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVPREVLINE)

        # CTRL+SHIFT+LEFT
        elif op == Caret.SELPREVWORD:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVPREVWORD)

        # CTRL+SHIFT+RIGHT
        elif op == Caret.SELNEXTWORD:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVNEXTWORD)

        # CTRL+SHIFT+HOME
        elif op == Caret.SELTEXTHOME:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVTEXTHOME)

        # CTRL+SHIFT+END
        elif op == Caret.SELTEXTEND:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVTEXTEND)

        # SHIFT+HOME
        elif op == Caret.SELLINEHOME:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVLINEHOME)

        # SHIFT+END
        elif op == Caret.SELLINEEND:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVLINEEND)

        # SHIFT+PAGEUP
        elif op == Caret.SELPAGEUP:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVPAGEUP)

        # SHIFT+PAGEDOWN
        elif op == Caret.SELPAGEDOWN:
            self.caret.start_selection()
            self.mov_operation(Caret.MOVPAGEDOWN)

        elif op == Caret.SELCANCEL:
            self.caret.selecting = False

    def mod_operation(self, op, text, pos=None):
        if op == Caret.MODINSERTCHAR:
            l, r = self.split_line(self.caret.line, self.caret.pos)
            self[self.caret.line] = unicode('{}{}{}'.format(l, text, r))
            self.caret.column += 1
            self.caret.memorize()

        elif op == Caret.MODREPLACECHAR:
            l, r = self.split_line(self.caret.line, self.caret.pos)
            if len(r) in (0, 1):
                r = ''
            else:
                r = r[1:]
            self[self.caret.line] = unicode('{}{}{}'.format(l, text, r))
            self.caret.column += 1
            self.caret.memorize()

        elif op == Caret.MODINSERTWORD:
            pass

        elif op == Caret.MODINSERTLINE:
            pass

        # BACKSPACE
        elif op == Caret.MODERASECHAR:
            if self.caret.column > 0:
                l, r = self.split_line(self.caret.line, self.caret.pos)
                if len(l) in (0, 1):
                    l = ''
                else:
                    l = l[:-1]
                self[self.caret.line] = unicode('{}{}{}'.format(l, text, r))
                self.caret.column -= 1

            elif not self.is_first_line:
                left = self[self.caret.line - 1]
                right = self[self.caret.line]
                self[self.caret.line -1] = unicode('{}{}'.format(left, right))
                del self[self.caret.line]
                self.caret.line -= 1
                self.caret.column = len(left)

            self.caret.memorize()

        # CTRL+BACKSPACE
        elif op == Caret.MODERASEWORD:
            pass
        elif op == Caret.MODERASELINE:
            pass
        # DELETE
        elif op == Caret.MODDELETECHAR:
            if self.caret.column < self.current_length:
                l, r = self.split_line(self.caret.line, self.caret.pos)
                if len(r) in (0, 1):
                    r = ''
                else:
                    r = r[1:]
                self[self.caret.line] = unicode('{}{}{}'.format(l, text, r))

            elif not self.is_last_line:
                left = self[self.caret.line]
                right = self[self.caret.line + 1]
                self[self.caret.line] = unicode('{}{}'.format(left, right))
                del self[self.caret.line + 1]

            self.caret.memorize()

        # CTRL+DELETE
        elif op == Caret.MODDELETEWORD:
            pass

        # SHIFT+DELETE
        elif op == Caret.MODDELETELINE:
            if not self.is_last_line:
                del self[self.caret.line]
                self.correct_column(self.caret.line)
            else:
                self[self.caret.line] = ''
                self.caret.column = 0
            self.caret.memorize()

        # RETURN
        elif op == Caret.MODINSERTNEWLINE:
            left, right = self.split_line(self.caret.line, self.caret.column)
            self[self.caret.line] = left
            self.caret.line += 1
            if self.is_last_line:
                self.lines.append(right)
            else:
                self.lines.insert(self.caret.line, right)
            self.caret.column = 0
            self.caret.memorize()

        # TAB
        elif op == Caret.MODINSERTTAB:
            pass
        elif op == Caret.MODDELSELECTION:
            pass
        elif op == Caret.MODMOVSELECTION:
            pass

    def split_line(self, line, col):
        ln = self.lines[line]
        if 0 < col < len(ln):
            left = ln[:col]
            right = ln[col:]
        elif col == 0:
            left = ''
            right = ln
        else:
            left = ln
            right = ''

        return left, right




"""the main library for rippy -- RIP"""

header_levels = {1: '#',
                2: '*',
                3: '=',
                4: '-',
                5: '^',
                6: '"'}


def anchor(name):
    """Return the anchor for a name."""
    if not name:
        return ''
    return '.. _{name}:\n\n'.format(name=name)


def doc(link, text=None):
    """Generate the :doc: link.

       If text, use the text for the link - otherwise just use the
       link itself as the link text.

    """
    text = text or link
    return ':doc:`{text} <{link}>`'.format(text=text, link=link)


def download(path, text):
    """Generate the rst download syntax"""
    return ':download:`{text} <{path}>`'.format(text=text, path=path)


def emphasis(text):
    """emphasize text"""
    return '*{text}*'.format(text=text)


def header(text, level):
    """Generate a header of a given level"""
    if not text:
        return ''
    uline = header_levels[level] * len(text)
    return '{text}\n{uline}\n\n'.format(text=text, uline=uline)


def note(text):
    """return a note"""
    return '.. note::\n\n   {text}\n'.format(text=text)

def p():
    """Create a paragraph break.  In ReST that is 2 newlines."""
    return '\n\n'


def ref(label, text=None):
    """Link to label with text or label as text"""
    text = text or label
    return ':ref:`{text} <{label}>`'.format(text=text, label=label)


def toctree(tree, maxdepth=1, *args):
    """return a toctree tag with tree items and args as toctree options"""
    pass


class Table(object):
    """Simple reST Table creator."""

    col_format = '{value:{fill}{align}{width}}'

    def __init__(self, title=None, headers=(), rows=(), anchor_text=None,
            heading_level=3):
        """Allow for justifiying in columns?

           The 'columns need to be as 'wide' as the widest
           data element within a cell.

           So we need to run through all the elements first, find the
           'widest' element and then padd everything to match that.

           If anchor_text is passed, an anchor to the table is created above
           the title (effectively a 'section' header).

           heading_level is the level of the title of the table being created.

        """
        self.col_widths = {}
        self.title = title
        self.rows = rows
        self.headers = headers
        self.anchor_text = anchor_text
        self.heading_level = heading_level

    def __call__(self):
        text = [self.title, ]

        if (not self.headers and not self.rows) or not self.headers:
            text.append('None\n\n')
            return ''.join(text)

        text.extend(self.headers)
        text.extend(self.rows)
        # after all the columns have been formatted...
        text.append('    '.join(self.lines))
        # XXX give a 'paragraph' between the table and whatever follows
        text.append(p())
        return '   '.join(text)


    @property
    def title(self):
        title = header(self._title, self.heading_level)
        if title:
            title = anchor(self.anchor_text) + title
        return title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def rows(self):
        """
        Return nicely formatted rows of data
        """
        result = []
        for row in self._rows:
            columns = []
            for idx, c in enumerate(row):
                size = self.col_widths.get(idx)
                columns.append(self.col_format.format(
                    value=c, fill=' ', align='<', width=size)
                               )
            result.append('    '.join(columns))
            result.append('\n')
        return result

    @rows.setter
    def rows(self, values):
        """
        Calculate max column widths from row data
        """
        self._rows = values
        for ridx, row in enumerate(values):
            columns = []
            for idx, column in enumerate(row):
                # ensure we have a string
                column = str(column)
                if column:
                    size = len(column)
                    if size > self.col_widths.get(idx, 0):
                        self.col_widths[idx] = size

    @property
    def headers(self):
        """
        Return nicely formatted headers, topped and tailed by lines
        of = signs
        """
        headers = []
        if not self._headers:
            return headers

        lines = '    '.join(self.lines)
        items = [lines, '\n']
        for idx, h in enumerate(self._headers):
            size = self.col_widths.get(idx)
            # center the header in the column
            headers.append(self.col_format.format(
                value=h, fill=' ', align='^',  width=size)
                           )
        items.append('    '.join(headers))
        items.append('\n')
        items.append(lines)
        items.append('\n')
        return items

    @headers.setter
    def headers(self, values):
        """
        Calculate max column widths from headers
        """
        self._headers = values
        for idx, v in enumerate(values):
            # pad the header values with extra space - looks better in tables
            size = len(v) + 14
            width = self.col_widths.get(idx, 0)
            self.col_widths[idx] = max(size, width)

    @property
    def lines(self):
        """
        Return a line of equals signs
        """
        lines = getattr(self, '_lines', None)
        if not lines:
            lines = []
            for idx, h in enumerate(self._headers):
                size = self.col_widths.get(idx)
                lines.append(
                    self.col_format.format(
                        value='', fill='=', align='<', width=size
                    )
                )
        self._lines = lines
        return lines


def table(*args, **kw):
    """
    Utility factory for creating tables in the same way as other objects.
    """
    return Table(*args, **kw)()

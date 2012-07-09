"""the main library for rippy -- RIP"""

header_levels = {1: '#',
                2: '*',
                3: '=',
                4: '-',
                5: '^',
                6: '"'}


def anchor(name):
    """Return the anchor for a name."""
    return '.. _%s:\n\n' % name


def doc(link, text=None):
    """Generate the :doc: link.

       If text, use the text for the link - otherwise just use the
       link itself as the link text.

    """
    return ':doc:`%(text)s <%(link)s>`' % {'text': text and text or link,
                                           'link': link}


def header(text, level):
    """Generate a header of a given level"""
    return '%(text)s\n%(uline)s\n\n' % {'text': text,
                                        'uline': header_levels.get(level) *\
                                                len(text)}


def emphasis(self, text):
    """emphasize text"""
    return '*%s*' % text


def note(text):
    """return a note"""
    return '.. note::\n\n   %(text)s\n' % {'text': text}


def p():
    """Create a paragraph break.  In reST that is 2 newlines."""
    return '\n\n'


def ref(label, text=None):
    """Link to label with text or label as text"""
    return ':ref:`%(text)s <%(label)s>`' % {'text': text and text or label,
                                             'label': label}


def toctree(tree, maxdepth=1, *args):
    """return a toctree tag with tree items and args as toctree options"""
    pass

class Table(object):
    """Simple reST Table creator."""

    col_format = '{0:{fill}{align}{width}}'

    def __init__(self, title, headers, rows, anchor_text=None,
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
        self.title = title
        self.rows = rows
        self.headers = headers
        self.anchor_text = anchor_text
        self.heading_level = heading_level
        self.col_widths = {}

    def __call__(self):
        anchor_text = ''
        text = []

        # if there is no title, the anchor is not useful
        text.append(self.title)

        if not self.rows:
            text.append('None\n\n')
            return ''.join(text)

        text.extend(self.headers)
        text.extend(self.rows)
        # after all the columns have been formatted...
        text.append(self.lines)
        # XXX give a 'paragraph' between the table and whatever follows
        text.append(p())
        return '   '.join(text)

    @property
    def title(self):
        if not self._title:
            return '\n'

        if anchor_text:
            anchor_text = anchor(self.anchor_text)

        table_header = header(title, self.heading_level)
        return anchor_text + table_header

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
                columns.append(self.col_format.format(c, fill=' ', align='<',
                    width=size))
            result.append('    '.join(columns))
            result.append('\n')
        return result

    @rows.setter
    def rows(self, values):
        """
        Calculate max column widths from row data
        """
        self._rows = rows
        for ridx, row in enumerate(values):
            columns = []
            for idx, column in enumerate(row):
                column = str(column) # ensure we have a string
                if column:
                    size = len(column)
                    if size > col_widths.get(idx, 0):
                        col_widths[idx] = size

    @property
    def headers(self):
        """
        Return nicely formatted headers, topped and tailed by lines
        of = signs
        """
        hdl = []
        items = []
        for idx, h in enumerate(self._headers):
            items.append(self.col_format.format(h, fill=' ', align='<',
                width=size))
        headers = "    ".join(headers)
        return [self.lines, ["\n"], headers, ["\n"], self.lines]


    @headers.setters:
        def headers(self, values)
        """
        Calculate max column widths from headers
        """
        self._headers = values
        for idx, v in enumerate(values):
            size = len(v) + 14
            self.col_widths[idx] = max(size, self.col_widths[idx])

    @property
    def lines(self):
        """
        Return a line of equals signs
        """
        lines = getattr(self, "_lines", None)
        if not lines:
            lines = []
            for idx, h in enumerate(self._headers):
                lines.append(
                    self.col_format.format('', fill='=', align='<', width=size)
                )
        self._lines = lines
        return lines


def table(*args, **kw):
    """
    Utility factory for creating tables in the same way as other objects.
    """
    return Table(*args, **kw)

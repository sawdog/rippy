"""the main library for rippy -- RIP"""

from string import join

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
    return ':ref: `%(text)s <%(label)s>`' % {'text': text and text or label,
                                             'label': label}


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
        self.headers = headers
        self.rows = rows
        self.anchor_text = anchor_text
        self.heading_level = heading_level
        self.text = []
        self.col_widths = {}

    def __call__(self):
        anchor_text = ''

        # if there is no title, the anchor is not useful
        self.text.append(self.title)

        if not self.rows:
            self.text.append('None\n\n')
            return ''.join(self.text)
        col_data = self.create_columns()

        # now begin formatting the table, with the headers
        hdl, items = self.format_columns()

        # there should be AT LEAST 2 spaces between 'columns' in the table
        text.append(join(hdl, '    '))
        text.append('\n')
        text.append(join(items, '    '))
        text.append('\n')
        text.append(join(hdl, '    '))
        text.append('\n')

        # now go back through the column_data and put it into the table
        for col in col_data:
            columns = []
            cols = col_data.get(col)
            for idx, c in enumerate(cols):
                size = col_widths.get(idx)
                columns.append(col_format.format(c, fill=' ', align='<',
                    width=size))

            text.append(join(columns, '    '))
            text.append('\n')

        # after all the columns have been formatted...
        text.append(join(hdl, '    '))
        # XXX give a 'paragraph' between the table and whatever follows
        text.append(p())
        return join(text, '   ')

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

    def create_columns(self):
        """
        Convert rows into columns accessible by row number.
        """
        col_data = {}
        # for each of the columns in the rows, we have to find the 'widest'
        for ridx, row in enumerate(self.rows):
            columns = []
            for idx, column in enumerate(row):
                column = str(column) # ensure we have a string
                if column:
                    size = len(column)
                    if size > col_widths.get(idx, 0):
                        col_widths[idx] = size
                    columns.append(column)
                else:
                    # XXX forgot why I'm doing this...duh
                    columns.append('....')

            col_data[ridx] = columns
        return col_data

    def create_headers(self):
        """
        """
        hdl = []
        items = []
        for idx, h in enumerate(self.headers):
            # XXX padding the header makes things look better....
            h = '      %s      ' % h
            size = len(h)
            # if the header is smaller then the largest column
            # use the widest...
            self.col_widths[idx] = max(size, self.col_widths[idx])

            # hval is just a bunch of '=' signs
            hval = self.col_format.format('', fill='=', align='<', width=size)
            hdl.append(hval)
            # now format the header
            items.append(self.col_format.format(h, fill=' ', align='<',
                width=size))
        return hdl, items


def table(*args, **kw):
    """
    Utility factory for creating tables in the same way as other objects.
    """
    return Table(*args, **kw)

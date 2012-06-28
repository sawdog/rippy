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

def header(header, level):
    """Generate a header of a given level"""
    return '%(text)s\n%(uline)s\n\n' % {'text': text,
                                        'uline': header_levels.get(level) *\
                                                len(text)}
def note(text):
    """return a note"""
    return '.. note::\n\n   %(text)s' % {'text': text}

def p():
    """Create a paragraph break.  In reST that is 2 newlines."""
    return '\n\n'

def _table(self, title, headers, rows, width=None, anchor_text=None,
        heading_level=3):
    """The 'columns need to be as 'wide' as the widest
       data element within a cell.

       So we need to run through all the elements first, find the
       'widest' element and then padd everything to match that.

       If anchor_text is passed, an anchor to the table is created above
       the title (effectively a 'section' header).

       heading_level is the level of the title of the table being created.

    """
    col_widths = {}
    anchor_text = ''
    text = []

    # if there is no title, the anchor is not useful
    if title:
        if anchor_text:
            anchor_text = anchor(anchor_text)
        text.append(anchor_text + header(title, heading_level))

    else:
        # this is needed to ensure the proper column header alignment
        text.append('\n')

    if not rows:
        text.append('None\n\n')
        return join(text, '')

    # now format the columns/rows...
    col_data = {}
    # for each of the columns in the rows, we have to find the 'widest'
    rcount = 0
    for row in rows:
        columns = []
        count = 0
        for column in row:
            if column:
                size = len(str(column))
                # if the column size is larger, replace the val
                if size > col_widths.get(count):
                    col_widths.update({count: size})
                columns.append(str(column))
            else:
                # XXX forgot why I'm doing this...duh
               columns.append('....')

            count += 1

        col_data.update({rcount: columns})
        rcount += 1

    # now begin formatting the table, with the headers
    col_format = '{0:{fill}{align}{width}}'
    count = 0
    hdl = []
    items = []
    for header in headers:
        # XXX padding the header makes things look better....
        header = '      %s      ' % header
        size = len(header)
        # if the header is smaller then the largest column
        # use the widest...
        if size < col_widths.get(count):
            size = col_widths.get(count)
        else:
            col_widths.update({count: size})

        # hval is just a bunch of '=' signs
        hval = col_format.format('', fill='=', align='<', width=size)
        hdl.append(hval)
        # now format the header
        items.append(col_format.format(header, fill=' ', align='<',
            width=size))
        count += 1

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
        count = 0
        for c in cols:
            size = col_widths.get(count)
            columns.append(col_format.format(c, fill=' ', align='<',
                width=size))
            count += 1

        text.append(join(columns, '    '))
        text.append('\n')

    # after all the columns have been formatted...
    text.append(join(hdl, '    '))
    # XXX give a 'paragraph' between the table and whatever follows
    text.append(p())
    return join(text, '   ')

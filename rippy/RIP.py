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

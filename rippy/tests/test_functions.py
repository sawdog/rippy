from unittest import TestCase


class TestFunctions(TestCase):
    """Test the various rst helper functions"""


    def test_no_anchor(self):
        """Only add anchors if we have names"""
        from rippy.RIP import anchor
        self.assertEqual(anchor(None), '')
        self.assertEqual(anchor(''), '')
        self.assertEqual(anchor(False), '')

    def test_anchor(self):
        """test the anchor function returns markup as expected"""
        from rippy.RIP import anchor
        expected = '.. _foo:\n\n'
        self.assertEqual(anchor('foo'), expected)

    def test_doc(self):
        """test the doc function returns markup as expected"""
        from rippy.RIP import doc
        # link with no title...
        expected = ':doc:`foo <foo>`'
        self.assertEqual(doc('foo'), expected)
        # link and title are different
        expected = ':doc:`bar <foo>`'
        self.assertEqual(doc('foo', 'bar'), expected)

    def test_download(self):
        """test the download function returns markup as expected"""
        from rippy.RIP import download
        expected = ':download:`download me <foo>`'
        self.assertEqual(download('foo', 'download me'), expected)

    def test_emphasis(self):
        """test the emphasis function returns markup as expected"""
        from rippy.RIP import emphasis
        expected = '*foo*'
        self.assertEqual(emphasis('foo'), expected)

    def test_header(self):
        """test the header function returns markup as expected for each
           of the 6 levels...

           Exceeding 6 causes a TypeError...

        """
        from rippy.RIP import header
        expected = 'foo\n%(level)s\n\n'
        self.assertEqual(header('foo', 1), expected % {'level': '###'})
        self.assertEqual(header('foo', 2), expected % {'level': '***'})
        self.assertEqual(header('foo', 3), expected % {'level': '==='})
        self.assertEqual(header('foo', 4), expected % {'level': '---'})
        self.assertEqual(header('foo', 5), expected % {'level': '^^^'})
        self.assertEqual(header('foo', 6), expected % {'level': '"""'})
        # no text returns ''
        self.assertEqual(header('', 1), '')
        self.assertRaises(KeyError, header, 'foo', 7)

    def test_note(self):
        """test the note function returns markup as expected"""
        from rippy.RIP import note
        expected = '.. note::\n\n   Notes are snafu.\n'
        self.assertEqual(note('Notes are snafu.'), expected)

    def test_p(self):
        """test the p function returns markup as expected"""
        from rippy.RIP import p
        expected = '\n\n'
        self.assertEqual(p(), expected)

    def test_ref(self):
        """test the ref function returns markup as expected"""
        from rippy.RIP import ref
        # just the label to reference
        expected = ':ref:`foo <foo>`'
        self.assertEqual(ref('foo'), expected)
        # label and link text are different
        expected = ':ref:`click me <foo>`'
        self.assertEqual(ref('foo', 'click me'), expected)


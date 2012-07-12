from unittest import TestCase

from rippy import RIP


class TestFunctions(TestCase):
    """Test the various rst helper functions"""

    def test_anchor(self):
        """test the anchor function returns markup as expected"""
        expected = '.. _foo:\n\n'
        self.assertEqual(RIP.anchor('foo'), expected)

    def test_doc(self):
        """test the doc function returns markup as expected"""
        # link with no title...
        expected = ':doc:`foo <foo>`'
        self.assertEqual(RIP.doc('foo'), expected)
        # link and title are different
        expected = ':doc:`bar <foo>`'
        self.assertEqual(RIP.doc('foo', 'bar'), expected)

    def test_download(self):
        """test the download function returns markup as expected"""
        expected = ':download:`download me <foo>`'
        self.assertEqual(RIP.download('foo', 'download me'), expected)

    def test_emphasis(self):
        """test the emphasis function returns markup as expected"""
        expected = '*foo*'
        self.assertEqual(RIP.emphasis('foo'), expected)

    def test_header(self):
        """test the header function returns markup as expected for each
           of the 6 levels...

           Exceeding 6 causes a TypeError...

        """
        expected = 'foo\n%(level)s\n\n'
        self.assertEqual(RIP.header('foo', 1), expected % {'level': '###'})
        self.assertEqual(RIP.header('foo', 2), expected % {'level': '***'})
        self.assertEqual(RIP.header('foo', 3), expected % {'level': '==='})
        self.assertEqual(RIP.header('foo', 4), expected % {'level': '---'})
        self.assertEqual(RIP.header('foo', 5), expected % {'level': '^^^'})
        self.assertEqual(RIP.header('foo', 6), expected % {'level': '"""'})
        self.assertRaises(TypeError, RIP.header, 'foo', 7)

    def test_note(self):
        """test the note function returns markup as expected"""
        expected = '.. note::\n\n   Notes are snafu.\n'
        self.assertEqual(RIP.note('Notes are snafu.'), expected)

    def test_p(self):
        """test the p function returns markup as expected"""
        expected = '\n\n'
        self.assertEqual(RIP.p(), expected)

    def test_ref(self):
        """test the ref function returns markup as expected"""
        # just the label to reference
        expected = ':ref:`foo <foo>`'
        self.assertEqual(RIP.ref('foo'), expected)
        # label and link text are different
        expected = ':ref:`click me <foo>`'
        self.assertEqual(RIP.ref('foo', 'click me'), expected)


from unittest import TestCase


class TestTable(TestCase):

    def get_target_class(self):
        from rippy.RIP import Table
        return Table

    def make_one(self):
        return self.get_target_class()()

    def test_default_anchor_text(self):
        table = self.make_one()
        self.assertEqual(table.anchor_text, None)

    def test_default_heading_level(self):
        table = self.make_one()
        self.assertEqual(table.heading_level, 3)

    def test_default_title(self):
        table = self.make_one()
        self.assertEqual(table.title, "\n")

    def test_default_rows(self):
        """Test the default Table behavior for the rows.

           By default the _rows is ()

           The setter will have no rows to calculate the max widths of the
           columns for the row data.

        """
        table = self.make_one()
        self.assertEqual(table.rows, [])
        self.assertEqual(table._rows, ())
        self.assertEqual(table.col_widths, {})

    def test_default_headers(self):
        """Test the default table behavior for the headers.

           By default the _headers will be ()

           The setter will have no column data for the max column widths.

        """
        table = self.make_one()
        self.assertEqual(table.headers, [])
        self.assertEqual(table._headers, ())
        self.assertEqual(table.col_widths, {})

    def test_table_call_with_defaults(self):
        """If there are no headers or rows, just returns 'None'"""
        table = self.make_one()
        self.assertEqual(table(), "\nNone\n\n")

    def test_headers(self):
        """Test the getting and setting of the table headers.

           setting the headers tracks the column widths - to ensure that
           when the table is drawn, the lines reflect that largest value
           (headers and rows) which has been set for the column.

           getting the headers formats them in rst markup, to render the
           headers as part of the table.

        """
        default_headers = ['One', 'Two', 'Three']
        table = self.make_one()
        table.headers = default_headers
        # setting the headers stuffs them into obj._headers
        self.assertEqual(table._headers, default_headers)
        # and determines the column widths - the headers are padded by
        # 14 to just make them more readable when drawn...IMNSHO.

        # first col is 17
        self.assertEqual(table.col_widths.get(0), 17)
        # second col is also 17
        self.assertEqual(table.col_widths.get(1), 17)
        # third col is 19
        self.assertEqual(table.col_widths.get(2), 19)

        # getting the headers formats them for the table with rst markup
        expected = ['=================    =================    ===================',
                '\n',
                '       One                  Two                  Three       ',
                '\n',
                '=================    =================    ===================',
                '\n']
        self.assertEqual(table.headers, expected)


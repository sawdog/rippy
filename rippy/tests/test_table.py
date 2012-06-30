from unittest import TestCase


class TestTable(TestCase):

    def get_target_class(self):
        from rippy.RIP import Table
        return Table

    def make_one(self):
        return self.get_target_class()(
            title=None,
            headers=None,
            rows=None)

    def test_no_title(self):
        Table = self.make_one()
        self.assertEqual(Table.title, "\n")

    def test_no_rows(self):
        Table = self.make_one()
        self.assertFalse(Table.rows)
        self.assertEqual(Table(), "\nNone\n\n")

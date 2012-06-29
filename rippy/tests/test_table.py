from unittest import TestCase


class TestTable(TestCase):

    def get_target_class(self):
        from rippy.RIP import Table
        return Table

    def test_no_title(self):
        Table = self.get_target_class()

"""Tests for SmartList sorting functionality."""

import unittest
import wx
from smart_list import SmartList, Column


class TestSorting(unittest.TestCase):
    """Test SmartList column sorting features."""

    def setUp(self):
        """Set up test fixtures."""
        self.app = wx.App()
        self.frame = wx.Frame(None)

    def tearDown(self):
        """Clean up test fixtures."""
        self.frame.Destroy()
        self.app.Destroy()

    def test_sort_by_string_column(self):
        """Test sorting by string attribute."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([
            Column(title="Name", model_field="name"),
            Column(title="Age", model_field="age")
        ])

        items = [
            {"name": "Charlie", "age": 30},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 35},
        ]
        lst.add_items(items)

        # Sort by name ascending
        lst.sort_by_column(0, reverse=False)
        self.assertEqual(lst.models[0]["name"], "Alice")
        self.assertEqual(lst.models[1]["name"], "Bob")
        self.assertEqual(lst.models[2]["name"], "Charlie")

        # Sort by name descending
        lst.sort_by_column(0, reverse=True)
        self.assertEqual(lst.models[0]["name"], "Charlie")
        self.assertEqual(lst.models[2]["name"], "Alice")

    def test_sort_by_numeric_column(self):
        """Test sorting by numeric attribute."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([
            Column(title="Name", model_field="name"),
            Column(title="Age", model_field="age")
        ])

        items = [
            {"name": "Charlie", "age": 30},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 35},
        ]
        lst.add_items(items)

        lst.sort_by_column(1, reverse=False)
        self.assertEqual(lst.models[0]["age"], 25)
        self.assertEqual(lst.models[1]["age"], 30)
        self.assertEqual(lst.models[2]["age"], 35)

    def test_toggle_sort(self):
        """Test toggle_sort switches direction."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([Column(title="Name", model_field="name")])

        items = [{"name": "B"}, {"name": "A"}, {"name": "C"}]
        lst.add_items(items)

        # First toggle: sort ascending
        lst.toggle_sort(0)
        self.assertEqual(lst.sort_column, 0)
        self.assertEqual(lst.sort_reverse, False)
        self.assertEqual(lst.models[0]["name"], "A")

        # Second toggle: reverse to descending
        lst.toggle_sort(0)
        self.assertEqual(lst.sort_reverse, True)
        self.assertEqual(lst.models[0]["name"], "C")

    def test_custom_sort_key(self):
        """Test sorting with custom sort_key function."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([
            Column(
                title="Name",
                model_field="name",
                sort_key=lambda x: x["name"].lower()  # Case-insensitive
            )
        ])

        items = [
            {"name": "charlie"},
            {"name": "Alice"},
            {"name": "BOB"},
        ]
        lst.add_items(items)

        lst.sort_by_column(0, reverse=False)
        self.assertEqual(lst.models[0]["name"], "Alice")
        self.assertEqual(lst.models[1]["name"], "BOB")
        self.assertEqual(lst.models[2]["name"], "charlie")

    def test_non_sortable_column(self):
        """Test that non-sortable columns raise error."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([
            Column(title="Name", model_field="name", sortable=False)
        ])

        items = [{"name": "A"}, {"name": "B"}]
        lst.add_items(items)

        with self.assertRaises(RuntimeError):
            lst.sort_by_column(0)

    def test_sort_state_persists_on_add(self):
        """Test that adding items maintains sort order."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([Column(title="Name", model_field="name")])

        lst.add_items([{"name": "C"}, {"name": "A"}])
        lst.sort_by_column(0, reverse=False)

        # Add new item
        lst.add_items([{"name": "B"}])

        # Should still be sorted
        self.assertEqual(lst.models[0]["name"], "A")
        self.assertEqual(lst.models[1]["name"], "B")
        self.assertEqual(lst.models[2]["name"], "C")

    def test_get_sort_state(self):
        """Test get_sort_state returns correct values."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([Column(title="Name", model_field="name")])

        lst.add_items([{"name": "A"}])

        # Initially unsorted
        self.assertEqual(lst.get_sort_state(), (None, False))

        # After sorting
        lst.sort_by_column(0, reverse=True)
        self.assertEqual(lst.get_sort_state(), (0, True))

    def test_clear_sort(self):
        """Test clear_sort removes sort state."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([Column(title="Name", model_field="name")])

        lst.add_items([{"name": "B"}, {"name": "A"}])
        lst.sort_by_column(0, reverse=False)

        # Clear sort
        lst.clear_sort()
        self.assertEqual(lst.get_sort_state(), (None, False))

    def test_reverse_sort_default(self):
        """Test reverse_sort parameter sets default direction."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([
            Column(title="Name", model_field="name", reverse_sort=True)
        ])

        lst.add_items([{"name": "A"}, {"name": "C"}, {"name": "B"}])

        # First toggle should use column's default (descending)
        lst.toggle_sort(0)
        self.assertEqual(lst.sort_reverse, True)
        self.assertEqual(lst.models[0]["name"], "C")

    def test_sort_with_callable_model_field(self):
        """Test sorting when model_field is a callable."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([
            Column(
                title="Full Name",
                model_field=lambda x: x["first"] + " " + x["last"]
            )
        ])

        items = [
            {"first": "Charlie", "last": "Brown"},
            {"first": "Alice", "last": "Smith"},
            {"first": "Bob", "last": "Jones"},
        ]
        lst.add_items(items)

        lst.sort_by_column(0, reverse=False)
        self.assertEqual(lst.models[0]["first"], "Alice")
        self.assertEqual(lst.models[1]["first"], "Bob")
        self.assertEqual(lst.models[2]["first"], "Charlie")

    def test_sort_empty_list(self):
        """Test sorting empty list doesn't crash."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([Column(title="Name", model_field="name")])

        # Should not raise error
        lst.sort_by_column(0, reverse=False)

    def test_sort_invalid_column_index(self):
        """Test sorting with invalid column index raises error."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([Column(title="Name", model_field="name")])

        lst.add_items([{"name": "A"}])

        with self.assertRaises(ValueError):
            lst.sort_by_column(5)

        with self.assertRaises(ValueError):
            lst.sort_by_column(-1)

    def test_sort_with_object_attributes(self):
        """Test sorting with object attributes (not dicts)."""

        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        lst = SmartList(parent=self.frame)
        lst.set_columns([
            Column(title="Name", model_field="name"),
            Column(title="Age", model_field="age")
        ])

        items = [
            Person("Charlie", 30),
            Person("Alice", 25),
            Person("Bob", 35),
        ]
        lst.add_items(items)

        lst.sort_by_column(0, reverse=False)
        self.assertEqual(lst.models[0].name, "Alice")
        self.assertEqual(lst.models[1].name, "Bob")
        self.assertEqual(lst.models[2].name, "Charlie")

    def test_sort_enabled_flag(self):
        """Test that sort_enabled flag controls sorting."""
        lst = SmartList(parent=self.frame)
        lst.set_columns([Column(title="Name", model_field="name")])

        items = [{"name": "B"}, {"name": "A"}]
        lst.add_items(items)

        # Disable sorting
        lst.sort_enabled = False

        # Should not raise error, but also should not sort
        # (handler would return early)
        original_order = [m["name"] for m in lst.models]
        lst.sort_enabled = True
        lst.sort_by_column(0)
        self.assertNotEqual([m["name"] for m in lst.models], original_order)


if __name__ == '__main__':
    unittest.main()

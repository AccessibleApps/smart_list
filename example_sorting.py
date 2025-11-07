"""Example demonstrating SmartList sorting functionality.

This example shows how to use the new sorting features:
- Sortable and non-sortable columns
- Custom sort keys
- Programmatic sorting
- Sort state management
"""

import wx
from smart_list import SmartList, Column


class Book:
    """Example model object."""

    def __init__(self, title, author, year, pages):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages


# Sample data
books = [
    Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, 180),
    Book("To Kill a Mockingbird", "Harper Lee", 1960, 324),
    Book("1984", "George Orwell", 1949, 328),
    Book("Pride and Prejudice", "Jane Austen", 1813, 432),
    Book("The Catcher in the Rye", "J.D. Salinger", 1951, 234),
]


class SortingDemoFrame(wx.Frame):
    """Demo frame showing sorting features."""

    def __init__(self):
        super(SortingDemoFrame, self).__init__(
            None, title="SmartList Sorting Demo", size=(800, 400)
        )

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create SmartList with sorting support
        self.lst = SmartList(parent=panel, style=wx.LC_REPORT)

        # Configure columns with different sorting options
        self.lst.set_columns([
            # Sortable column with case-insensitive sorting
            Column(
                title="Title",
                model_field="title",
                width=200,
                sortable=True,
                sort_key=lambda book: book.title.lower()
            ),
            # Sortable column (default)
            Column(
                title="Author",
                model_field="author",
                width=200,
                sortable=True
            ),
            # Sortable numeric column, default descending
            Column(
                title="Year",
                model_field="year",
                width=100,
                sortable=True,
                reverse_sort=True
            ),
            # Sortable numeric column
            Column(
                title="Pages",
                model_field="pages",
                width=100,
                sortable=True
            ),
            # Non-sortable column
            Column(
                title="Actions",
                model_field=lambda book: "View",
                width=100,
                sortable=False
            )
        ])

        # Add books to list
        self.lst.add_items(books)

        sizer.Add(self.lst.control.control, 1, wx.EXPAND | wx.ALL, 5)

        # Add control buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Sort buttons
        sort_title_btn = wx.Button(panel, label="Sort by Title")
        sort_title_btn.Bind(wx.EVT_BUTTON, lambda e: self.lst.sort_by_column(0))
        button_sizer.Add(sort_title_btn, 0, wx.ALL, 5)

        sort_year_btn = wx.Button(panel, label="Sort by Year")
        sort_year_btn.Bind(wx.EVT_BUTTON, lambda e: self.lst.sort_by_column(2))
        button_sizer.Add(sort_year_btn, 0, wx.ALL, 5)

        # Add book button
        add_btn = wx.Button(panel, label="Add Book")
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_book)
        button_sizer.Add(add_btn, 0, wx.ALL, 5)

        # Clear sort button
        clear_btn = wx.Button(panel, label="Clear Sort")
        clear_btn.Bind(wx.EVT_BUTTON, lambda e: self.lst.clear_sort())
        button_sizer.Add(clear_btn, 0, wx.ALL, 5)

        # Show state button
        state_btn = wx.Button(panel, label="Show Sort State")
        state_btn.Bind(wx.EVT_BUTTON, self.on_show_state)
        button_sizer.Add(state_btn, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER)

        # Status text
        self.status = wx.StaticText(panel, label="Click column headers to sort!")
        sizer.Add(self.status, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        panel.SetSizer(sizer)
        self.Centre()

    def on_add_book(self, event):
        """Add a new book to demonstrate sort persistence."""
        new_book = Book("New Book", "New Author", 2023, 250)
        self.lst.add_items([new_book])
        self.status.SetLabel("Added new book. Sort order maintained!")

    def on_show_state(self, event):
        """Display current sort state."""
        column, reverse = self.lst.get_sort_state()
        if column is None:
            msg = "List is not sorted"
        else:
            direction = "descending" if reverse else "ascending"
            col_name = self.lst.columns[column].title
            msg = f"Sorted by: {col_name} ({direction})"
        self.status.SetLabel(msg)


def main():
    """Run the demo application."""
    app = wx.App()
    frame = SortingDemoFrame()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

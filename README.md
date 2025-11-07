# Smart List

Model-based list control for wxPython with virtual scrolling support for large datasets.

## Features

- **Model-based**: Display any Python object (classes, dicts, dataclasses)
- **Virtual lists**: Handle millions of items without loading into memory
- **Cross-platform**: Automatic ListView (Windows/Linux) or DataView (macOS)
- **Flexible columns**: Extract values via attributes, dict keys, or callables
- **Performance optimized**: Windows IAT hooking prevents UIA enumeration delays

## Installation

```bash
uv add smart_list
# or
pip install smart_list
```

## Usage

### Basic List

For datasets that fit in memory (< 10K items):

```python
import wx
from smart_list import SmartList, Column

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [Person("Alice", 30), Person("Bob", 25)]

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Smart List", size=(400, 300))
        panel = wx.Panel(self)

        self.list = SmartList(parent=panel, style=wx.LC_REPORT)
        self.list.set_columns([
            Column(title="Name", model_field="name", width=150),
            Column(title="Age", model_field="age", width=100)
        ])
        self.list.add_items(people)
        self.Show()

app = wx.App()
MyFrame()
app.MainLoop()
```

### Virtual Lists

For large datasets (> 10K items) or database-backed data:

```python
from smart_list import VirtualSmartList, Column

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, size=(400, 300))
        panel = wx.Panel(self)

        # Example: Database with 1 million rows
        def get_item(index):
            return db.query("SELECT * FROM users LIMIT 1 OFFSET ?", index)

        def load_batch(start, end):
            # Optional: batch loading for performance
            return db.query("SELECT * FROM users LIMIT ? OFFSET ?", end - start + 1, start)

        self.list = VirtualSmartList(
            parent=panel,
            style=wx.LC_REPORT,
            get_virtual_item=get_item,
            update_cache=load_batch  # Optional but recommended
        )
        self.list.set_columns([
            Column(title="ID", model_field="id"),
            Column(title="Name", model_field="name"),
            Column(title="Email", model_field="email")
        ])
        self.list.update_count(1000000)  # Total rows
        self.Show()
```

**Virtual list requirements:**
- Provide `get_virtual_item(index)` callback
- Call `update_count(n)` with total items
- Optionally provide `update_cache(start, end)` for batch loading

## Column Field Resolution

Columns extract values using three strategies:

```python
# 1. Attribute access
Column(title="Name", model_field="name")  # obj.name

# 2. Dict key access
Column(title="Email", model_field="email")  # obj["email"]

# 3. Callable
Column(title="Full Name", model_field=lambda p: f"{p.first} {p.last}")
Column(title="Age", model_field=lambda p: datetime.now().year - p.birth_year)
```

Resolution order: callable → attribute → dict key

## Column Sorting

SmartList supports column-based sorting with visual indicators. Users can click column headers to sort, or you can sort programmatically.

### Basic Sorting

By default, all columns are sortable:

```python
from smart_list import SmartList, Column

# All columns are sortable by default
list.set_columns([
    Column(title="Name", model_field="name"),
    Column(title="Age", model_field="age")
])

# Users can click headers to sort
# First click: ascending
# Second click: descending
# Click different column: sort by that column
```

### Non-Sortable Columns

Disable sorting for specific columns:

```python
Column(
    title="Actions",
    model_field=get_actions,
    sortable=False  # Clicking header does nothing
)
```

### Custom Sort Keys

Use `sort_key` for custom sort logic:

```python
# Case-insensitive string sorting
Column(
    title="Name",
    model_field="name",
    sort_key=lambda x: x["name"].lower()
)

# Sort by computed value
Column(
    title="Authors",
    model_field=format_authors,  # Display: "Smith, Jones"
    sort_key=lambda x: len(x["authors"])  # Sort: by count
)

# Sort by nested field
Column(
    title="Location",
    model_field="address.city",
    sort_key=lambda x: x.address.city if x.address else ""
)
```

### Default Sort Direction

Set default sort direction for a column:

```python
# Numeric columns often default to descending
Column(
    title="Downloads",
    model_field="downloads",
    reverse_sort=True  # First click sorts descending
)
```

### Programmatic Sorting

```python
# Sort by column index
list.sort_by_column(column_index=0, reverse=False)

# Toggle sort (same as clicking header)
list.toggle_sort(column_index=1)

# Check sort state
column_idx, is_reversed = list.get_sort_state()
if column_idx is not None:
    print(f"Sorted by column {column_idx}")

# Clear sorting
list.clear_sort()
```

### Sort Persistence

Sort order is maintained when adding items:

```python
list.sort_by_column(0)  # Sort by first column
list.add_items([new_item1, new_item2])  # Items inserted in sorted position
```

### Visual Indicators

- **ListView** (Windows/Linux): Shows ▲ (ascending) or ▼ (descending) in header
- **DataView** (macOS): Uses native sort indicator

### Sorting Limitations

- **Virtual lists** do not support sorting (client-side sorting not feasible for large datasets)
- Mixed-type columns may fail to sort (e.g., mixing strings and numbers)
- Sort keys should handle None values gracefully

### Complete Example

```python
import wx
from smart_list import SmartList, Column

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

books = [
    Book("1984", "George Orwell", 1949),
    Book("Brave New World", "Aldous Huxley", 1932),
    Book("Animal Farm", "George Orwell", 1945),
]

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, size=(600, 400))
        panel = wx.Panel(self)

        self.list = SmartList(parent=panel, style=wx.LC_REPORT)
        self.list.set_columns([
            # Case-insensitive title sorting
            Column(
                title="Title",
                model_field="title",
                width=200,
                sort_key=lambda b: b.title.lower()
            ),
            # Author sorting (default)
            Column(
                title="Author",
                model_field="author",
                width=150
            ),
            # Year sorting, default descending (newest first)
            Column(
                title="Year",
                model_field="year",
                width=100,
                reverse_sort=True
            ),
        ])
        self.list.add_items(books)
        self.Show()

app = wx.App()
MyFrame()
app.MainLoop()
```

## API Reference

### SmartList

| Method | Description |
|--------|-------------|
| `set_columns(columns)` | Configure column definitions |
| `add_items(items)` | Add multiple items (uses freeze/thaw) |
| `add_item(item)` | Add single item |
| `get_items()` | Return all model objects |
| `update_models(models)` | Update or add models, refresh display |
| `insert_item(index, item)` | Insert at specific position |
| `delete_item(item)` | Remove item by value |
| `update_item(item)` | Refresh single item display |
| `get_selected_items()` | Iterator of selected models |
| `get_selected_item()` | First selected model or None |
| `select_model(item)` | Select item by value |
| `find_index_of_item(model)` | Get list index for model |
| `clear()` | Remove all items |
| `sort_by_column(column_index, reverse)` | Sort by column index |
| `toggle_sort(column_index)` | Toggle sort or sort by new column |
| `get_sort_state()` | Get (column_index, reverse) tuple |
| `clear_sort()` | Clear sort state and indicators |

### VirtualSmartList

Inherits SmartList methods plus:

| Method | Description |
|--------|-------------|
| `update_count(count)` | Set total number of virtual items |
| `refresh()` | Refresh display and clear cache |
| `find_index_of_item(item)` | Linear search for item (O(n)) |

**Constructor requirements:**
- `get_virtual_item(index)`: Required callback returning model for index
- `update_cache(from_row, to_row)`: Optional batch loader returning list of models

### Column

```python
Column(
    title="Header",
    model_field="field",
    width=100,
    sortable=True,
    sort_key=None,
    reverse_sort=False
)
```

| Parameter | Description |
|-----------|-------------|
| `title` | Column header text |
| `model_field` | Field name (str) or callable for extracting values |
| `width` | Column width in pixels (-1 for auto) |
| `sortable` | Whether column can be sorted (default: True) |
| `sort_key` | Custom callable for extracting sort value (optional) |
| `reverse_sort` | Default sort direction, True=descending (default: False) |

## Performance Considerations

### When to Use Virtual Lists

| Scenario | Use | Reason |
|----------|-----|--------|
| < 10K items in memory | `SmartList` | Simple, full API |
| > 10K items | `VirtualSmartList` | Memory efficient |
| Database-backed | `VirtualSmartList` | Load on demand |
| Frequent add/remove | `SmartList` | O(1) index lookup |
| Read-only large dataset | `VirtualSmartList` | No memory overhead |

### Bulk Operations

Use `add_items()` instead of multiple `add_item()` calls. The freeze/thaw decorator prevents UI flicker:

```python
# Good: Single batch
list.add_items(1000_items)

# Bad: 1000 separate updates
for item in items:
    list.add_item(item)
```

### Windows Performance

On Windows 8/10, the library automatically installs an IAT hook to fix a UIA bug that enumerates all virtual list items. Without this fix, virtual lists with > 100K items experience multi-second delays.

## Platform Differences

The library provides a unified API but uses different underlying controls:

| Platform | Control | Reason |
|----------|---------|--------|
| macOS | DataView | Required for accessibility |
| Windows | ListView | Better performance |
| Linux | ListView | Better performance |

Code using SmartList works identically on all platforms.

## Requirements

- wxPython (>= 4.0)
- frozendict
- resource_finder
- pywin32 (Windows only, for IAT hooking)
# 🧾 Sales Validation & Multi-Department Reporting System

This Python program performs comprehensive validation and reporting of sales data. It is designed to handle multiple departments, patched price lists, and detect discrepancies in sales totals. Ideal for small businesses or inventory managers who need to analyze data across departments.

---

## 🚀 Features

### ✅ Sales Validation
- Ensures each sale has a valid item and that total ≈ unit price × quantity (±0.01 margin allowed).
- Detects incorrect totals and unknown item types.

### 📊 Department-wise Reporting
- Groups sales by department.
- Applies price **patches** (overrides) for each department.
- Uses **base price** + **patch** to generate department-specific reports.

### 🧠 Functions Overview

| Function | Description |
|---------|-------------|
| `is_valid_sale()` | Checks if a sale's item exists and total is valid. |
| `flag_invalid_sales()` | Returns a list of invalid sales. |
| `generate_sales_report()` | Returns summary report for a department. |
| `patch_item_price()` | Applies patch prices on top of base price. |
| `generate_sales_reports()` | Aggregates reports and errors for all departments. |

---

## 📦 Example Usage

```python
if __name__ == "__main__":
    price = {"apple": 2.0, "orange": 3.0, "tangerine": 4.0}
    patch = {
        "dep2": {"carrot": 2.5}
    }
    sales = [
        ["dep1", "apple", 1, 2.0],
        ["dep1", "apple", 3, 6.0],
        ["dep1", "orange", 1, 2.0],        # Invalid: total too low
        ["dep1", "carrot", 1, 8.0],        # Invalid: unknown item
        ["dep2", "orange", 3, 9.0],
        ["dep2", "carrot", 2, 5.0],
        ["dep2", "apricot", 1, 9.0],       # Invalid: unknown item
        ["dep3", "apricot", 1, 9.0],       # Invalid: unknown item
    ]

    for report in generate_sales_reports(price, patch, sales):
        print(report)
## 🖥 Sample Output

('dep1', 
 {'apple': (4, 2, 4.0, 0), 
  'orange': (0, 1, 0.0, 1), 
  'tangerine': (0, 0, 0.0, 0), 
  'carrot': (0, 1, 0.0, 1)}, 
 [['orange', 1, 2.0], ['carrot', 1, 8.0]])

('dep2',
 {'apple': (0, 0, 0.0, 0), 
  'orange': (3, 1, 9.0, 0), 
  'tangerine': (0, 0, 0.0, 0), 
  'carrot': (2, 1, 5.0, 0), 
  'apricot': (0, 1, 0.0, 1)}, 
 [['apricot', 1, 9.0]])

('dep3',
 {'apple': (0, 0, 0.0, 0), 
  'orange': (0, 0, 0.0, 0), 
  'tangerine': (0, 0, 0.0, 0), 
  'apricot': (0, 1, 0.0, 1)}, 
 [['apricot', 1, 9.0]])

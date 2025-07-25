'''
    Validates a single sale by checking if the item type exists in the price dictionary and if
    the sale total matches the expected total based on item price and quantity.

    Arguments:
        price (dict): Dictionary mapping item_type(str) to respective unit prices (float).
        item_type(str): Type of item being sold.
        item_quantity(int): Number of units sold.
        sale_total (float): Recorded total amount for sale.

    Returns:
        bool(True): if the sale is valid (item exists and total is within 0.01 of expected), False otherwise.
'''
def is_valid_sale(price, item_type, item_quantity, sale_total):
    if item_type not in price:
        return False
    
    expected_total = price[item_type] * item_quantity
    # allow a small margin for floating-point comparison
    return abs(expected_total - sale_total) < 0.01


    '''
    Identifies invalid sales from a list of sales by using `is_valid_sale()` function to verify each sale.

    Arguments:
        price(dict): Dictionary containing the mapping of item types(str) to their unit prices(float).
        sales(list): List of sales, where each sale is a list containing `item_type`(str), `item_quantity`(int), `sale_total`(float).

    Returns: 
        list : List of invalid sales, where each sale is a list containing `item_type`(str), `item_quantity`(int), `sale_total`(float).
    '''
def flag_invalid_sales(price, sales):
    invalid_sales = []
    for sale in sales:
        item_type, item_quantity, sale_total = sale
        if not is_valid_sale(price, item_type, item_quantity, sale_total):
            invalid_sales.append(sale)
    return invalid_sales

    '''
    Generates a comprehensive sales report summarising units sold, sales made, average income per valid sale and errors for each item type.
    Verify whether sale is valid using `is_valid_sale()` function.

    Arguments:
        price(dict): Dictionary mapping `item_type`(str) to it's respective `unit_price`(float).
        sales(dict): List of sales where each sale is a list containing `item_type`(str), `item_quantity`(int), `sale_total`(float).

    Returns:
        dict : Dictionary mapping `item_type`(str) to tuples containing `units_sold`(int), `sales_made`(int), `average_income`(float) and `errors`(int). 
        units_sold(int): Total units sold in valid sales.
        sales_made(int): Total number of sales attempted.
        average_income(float): Average income per valid sale.
        errors(int): Number of invalid sales.
    
    1. Average income is only calculated on valid sales. If no valid sales exist, then it is 0.0.
    2. Sales are considered invalid if the item is not in `price` OR if the sale total deviates from the expected total by more than the permissible range of 0.01.
    3. The reports include all items from `price` dictionary , even if they have no sales.
    4. Items not in `price` but present in `sales` are included in the report with the appropriate error counts.
    '''
def generate_sales_report(price, sales):

    report = {}

    # initialize report for all items
    for item in price:
        report[item] = {
            "units_sold": 0,
            "sales_made": 0,
            "total_income": 0.0,
            "errors": 0
        }

    # according to the sale report and accumulation 
    for sale in sales:
        item_type, item_quantity, sale_total = sale
        
        
        # if there is some products not in the price table ,and then initialization the report fields 
        if item_type not in report:
            report[item_type] = {
                "units_sold": 0,
                "sales_made": 0,
                "total_income": 0.0,
                "errors": 0
            }

        # count tatoal sales made fot this item
        report [item_type]['sales_made'] += 1
        
        if not is_valid_sale(price, item_type, item_quantity, sale_total):
            # count the invalid sales
            report[item_type]['errors'] += 1
        else:
            report [item_type]['units_sold'] += item_quantity
            report [item_type]['total_income'] += sale_total

    # compile final summary output
    final_summary= {}
    for item in report:
        units_sold = report[item]['units_sold']
        sales_made = report[item]['sales_made']
        errors = report[item]['errors']
        valid_sales= sales_made - errors

        # calculate average income from valid sales
        if valid_sales > 0 :
            average_income = report[item]['total_income']/valid_sales
        else:
            average_income = 0.0

        # each item maps to summary values
        final_summary[item] = (units_sold,sales_made,average_income,errors)

    return final_summary

    '''
    Creates a new price dictionary by combining the base price dictionary with a patch dictionary, updating or adding 
    item prices as specified in the patch.

    Arguments:
        price(dict): Dictionary mapping item types(str) to respective base unit prices(float).
        patch(dict): Dictionary mapping item types(str) to respective updated unit prices(float) to override or add to the base prices.

    Returns:
        dict : A new dictionary containing all items from `price` with any updated prices from `patch` and additional items as introduced by `patch`.
    '''
# combine the price table and patch table
def patch_item_price(price, patch):
    combined = price.copy()
    combined.update(patch)
    return combined

    '''
    Generates department-specific sales reports by grouping sales by department, applying department-specific price 
    patches and producing a report, along with an invalid sales list for each department using `generate_sales_report()` function along with
    `flag_invalid_sales()` function.

    Arguments:
        price(dict): Dictionary mapping item types(str) to their base unit prices(float).
        patch(dict): Dictionary mapping department names(str) to dictionaries of item types(str) and their updated unit prices(float).
        sales(list): List of total sales, where each sale is a list containing `department`(str), `item_type`(str), `quantity`(str) and `total`(float).
    
    Returns:
        list: List of tuples `(department, report, invalid)` where:
        department(str) : The department name.
        report(dict): The sales report for the department, as returned by 'generate_sales_report()` function.
        invalid(list): List of invalid sales for the department, as compiled by 'flag_invalid_sales()` function.
    
   
    1.Sales are grouped by department before processing.
    2. Each department uses a price dictionary, combining the base `price` with its specific `patch` (as applicable),created by `patch_item_price()` function.
    3. If a department has no applicable patch in `patch`, it follows that the base `price` remains unchanged.
    4. The report and the invalid sales list for each department contain all the relevant items, including those not in the patched price dictionary.
    '''
# according to the sales report for each department
def generate_sales_reports(price, patch, sales):
    department_sales = {}

    # arrange the sales report for each department
    for department, item_type, quantity, total in sales:
        if department not in department_sales:
            department_sales[department] = []
        department_sales[department].append([item_type,quantity,total])
    
    reports = []

    # make the report for each department and check the wrong sale
    for department, department_sales_list in department_sales.items():
        department_patch = patch.get(department, {})
        department_prices = patch_item_price(price, department_patch)

        report= generate_sales_report(department_prices, department_sales_list)
        invalid = flag_invalid_sales(department_prices, department_sales_list)

        reports.append((department,report,invalid))
    
    return reports

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    price = {"apple": 2.0, "orange": 3.0, "tangerine": 4.0}
    patch = {
            "dep2": {"carrot": 2.5}
        }
    sales = [
            ["dep1","apple", 1, 2.0],
            ["dep1","apple", 3, 6.0],
            ["dep1","orange", 1, 2.0],
            ["dep1","carrot", 1, 8.0],
            ["dep2","orange", 3, 9.0],
            ["dep2","carrot", 2, 5.0],
            ["dep2","apricot", 1, 9.0],
            ["dep3","apricot", 1, 9.0],
        ]

    print("SALES REPORTS")
    for report in generate_sales_reports(price,patch,sales):
        print(report)

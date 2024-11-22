# import frappe
# from frappe.utils import getdate

# def execute(filters=None):
#     # Define columns for the report
#     columns = [
#         {"label": "Medicine", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 150},
#         {"label": "Batch ID", "fieldname": "batch_id", "fieldtype": "Link", "options": "Batch", "width": 120},
#         {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Quantity", "fieldname": "batch_qty", "fieldtype": "Float", "width": 100},
#         {"label": "Expiry Date", "fieldname": "expiry_date", "fieldtype": "Date", "width": 120},
#     ]

#     # Fetch data
#     data = get_data(filters)

#     return columns, data


# def get_data(filters):
#     # Prepare conditions for filters
#     conditions = {}
#     if filters.get("medicine"):
#         conditions["item"] = filters.get("medicine")
#     if filters.get("warehouse"):
#         conditions["warehouse"] = filters.get("warehouse")
#     if filters.get("expiry_date"):
#         conditions["expiry_date"] = ("<=", getdate(filters["expiry_date"]))

#     # Fetch batches based on the filters
#     batches = frappe.get_all('Batch', 
#                              filters=conditions, 
#                              fields=['item', 'batch_id', 'expiry_date'])

#     data = []

#     # Loop through batches to get stock data from Stock Ledger Entry
#     for batch in batches:
#         # Fetch stock ledger entries for each batch and warehouse
#         sle_filters = {
#             "batch_no": batch["batch_id"],
#             "item_code": batch["item"]
#         }

#         if filters.get("warehouse"):
#             sle_filters["warehouse"] = filters["warehouse"]

#         stock_entries = frappe.get_all('Stock Ledger Entry', filters=sle_filters, fields=['warehouse', 'actual_qty'])

#         # Loop through stock entries and add to data
#         for entry in stock_entries:
#             data.append({
#                 "item": batch["item"],
#                 "batch_id": batch["batch_id"],
#                 "warehouse": entry["warehouse"],
#                 "batch_qty": entry["actual_qty"],
#                 "expiry_date": batch["expiry_date"]
#             })

#     return data


import frappe
from frappe.utils import getdate

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"label": "Medicine", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Batch ID", "fieldname": "batch_id", "fieldtype": "Link", "options": "Batch", "width": 120},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"label": "Quantity", "fieldname": "batch_qty", "fieldtype": "Float", "width": 100},
        {"label": "Expiry Date", "fieldname": "expiry_date", "fieldtype": "Date", "width": 120},
    ]

    # Fetch data
    data = get_data(filters)
    frappe.msgprint(f"Fetched Data: {data}")  # Debugging line

    return columns, data


def get_data(filters):
    conditions = []
    if filters.get("medicine"):
        conditions.append({"item_code": filters["medicine"]})
    if filters.get("warehouse"):
        conditions.append({"warehouse": filters["warehouse"]})
    if filters.get("expiry_date"):
        conditions.append({"expiry_date": ("<=", getdate(filters["expiry_date"]))})

    # Debugging line to show conditions
    frappe.msgprint(f"Conditions: {conditions}")

    # Get all batches with their stock quantities
    batches = frappe.get_all('Batch', filters=conditions, fields=['item', 'batch_id', 'expiry_date'])

    # Debugging line to show fetched batches
    frappe.msgprint(f"Batches: {batches}")

    # Now, we need to calculate stock quantities for each batch and warehouse
    data = []

    for batch in batches:
        # Get stock ledger entries for each batch and warehouse
        sle_filters = {
            "batch_no": batch['batch_id'],
            "item_code": batch['item'],
        }

        if filters.get("warehouse"):
            sle_filters["warehouse"] = filters["warehouse"]

        # Fetch stock ledger entries for this batch
        stock_entries = frappe.get_all('Stock Ledger Entry', filters=sle_filters, fields=['warehouse', 'actual_qty'])

        # Debugging line to show stock entries
        frappe.msgprint(f"Stock Entries for batch {batch['batch_id']}: {stock_entries}")

        for entry in stock_entries:
            data.append({
                "item": batch['item'],
                "batch_id": batch['batch_id'],
                "warehouse": entry['warehouse'],
                "batch_qty": entry['actual_qty'],
                "expiry_date": batch['expiry_date'],
            })

    # Debugging line to show the final data
    frappe.msgprint(f"Final Data: {data}")
    
    return data

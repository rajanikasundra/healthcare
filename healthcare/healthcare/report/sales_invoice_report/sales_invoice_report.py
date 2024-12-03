import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Invoice Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Invoice Number", "fieldname": "invoice_number", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Quantity", "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    # Build dynamic conditions
    conditions = []
    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("si.posting_date BETWEEN %(from_date)s AND %(to_date)s")
    if filters.get("customer"):
        conditions.append("si.customer = %(customer)s")
    conditions.append("sii.item_group = 'Medicine'")  # Filter for medicines

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Use SQL to join parent and child tables
    data = frappe.db.sql(
        f"""
        SELECT
            si.posting_date,
            si.name AS invoice_number,
            si.customer,
            sii.item_name,
            sii.qty,
            sii.amount
        FROM
            `tabSales Invoice` si
        INNER JOIN
            `tabSales Invoice Item` sii ON si.name = sii.parent
        WHERE
            {where_clause}
        ORDER BY
            si.posting_date DESC
        """,
        filters,
        as_dict=True
    )

    return data

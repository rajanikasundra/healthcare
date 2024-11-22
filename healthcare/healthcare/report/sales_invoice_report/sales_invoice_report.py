# Copyright (c) 2024, sigzen and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    # Define report columns
    columns = [
        {"label": "Invoice Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Invoice ID", "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
        {"label": "Customer", "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
        {"label": "Service Type", "fieldname": "service_type", "fieldtype": "Data", "width": 150},
        # {"label": "Patient Age", "fieldname": "patient_age", "fieldtype": "Int", "width": 100},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
    ]

    # Fetch data
    data = get_data(filters)

    return columns, data


def get_data(filters):
    # Build the query dynamically with filters
    conditions = []
    if filters.get("service_type"):
        conditions.append("si_item.item_code = %(service_type)s")
    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Query to fetch data
    data = frappe.db.sql(
        f"""
        SELECT
            si.posting_date,
            si.name,
            si.customer_name,
            si_item.item_code AS service_type,
            p.age AS patient_age,
            si_item.amount AS revenue
        FROM
            `tabSales Invoice` si
        JOIN
            `tabSales Invoice Item` si_item ON si.name = si_item.parent
        LEFT JOIN
            `tabPatient` p ON si.customer = p.name
        WHERE
            {where_clause}
        ORDER BY
            si.posting_date DESC
        """,
        filters or {},
        as_dict=True,
    )

    return data


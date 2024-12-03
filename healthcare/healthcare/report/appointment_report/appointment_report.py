# Copyright (c) 2024, sigzen and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Doctor", "fieldname": "custom_doctor", "fieldtype": "Link", "options": "Doctor", "width": 200},
        {"label": "Date", "fieldname": "scheduled_time", "fieldtype": "Date", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Select", "width": 120},
        {"label": "Patient", "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
    ]

    data = get_data(filters)

    return columns, data

def get_data(filters):
    filters = filters or {}
    conditions = []
    print(filters)
    print("\n\n")
    print(conditions)
    if filters.get("custom_doctor"):
        conditions.append(["custom_doctor", "=", filters.get("custom_doctor")])
    if filters.get("from_date") and filters.get("to_date"):
        conditions.append(["scheduled_time", "between", [filters.get("from_date"), filters.get("to_date")]])
    if filters.get("status"):
        conditions.append(["status", "=", filters.get("status")])
    print("\n\n")
    print(conditions)
    appointments = frappe.get_all(
        "Appointment",
        fields=["custom_doctor", "scheduled_time", "status", "customer_name"],
        filters=conditions,
        order_by="scheduled_time desc"
    )

    return appointments

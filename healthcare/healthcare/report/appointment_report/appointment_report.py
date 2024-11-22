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
    
    conditions = []
    if filters.get("custom_doctor"):
        conditions.append("custom_doctor = %(custom_doctor)s")
    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("scheduled_time BETWEEN %(from_date)s AND %(to_date)s")
    if filters.get("status"):
        conditions.append("status = %(status)s")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

  
    data = frappe.db.sql(
        f"""
        SELECT
            
            custom_doctor,
            scheduled_time,
            status,
            customer_name
        FROM
            `tabAppointment`
        WHERE
            {where_clause}
        ORDER BY
            scheduled_time DESC
        """,
        filters,
        as_dict=True
    )

    return data


















































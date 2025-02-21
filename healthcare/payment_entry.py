import frappe

#  appointement to sales invoice

@frappe.whitelist()
def generate_appointment_invoice(appointment_name):
    
  
    appointment = frappe.get_doc('Appointment', appointment_name)

 
    if not appointment.customer_name:
        frappe.throw("Customer is required to create a Sales Invoice.")


    sales_invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "custom_appoinment" : appointment_name,
        "customer": appointment.custom_patient,
        "posting_date": frappe.utils.today(),
        "additional_discount_percentage" : appointment.custom_discount,
        "due_date": frappe.utils.add_days(frappe.utils.today(), 2),
        "items": [
            {
                "item_code": "Doctor Charges",  
                "qty": 1,
                "rate": appointment.custom_charges  
            }
        ]
    })


    # appointment.status = 'Completed'
    # appointment.save()
    
    sales_invoice.insert(ignore_permissions=True)

    return sales_invoice.name

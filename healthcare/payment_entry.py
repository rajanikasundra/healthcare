import frappe


# @frappe.whitelist()
# def create_payment_entry(source_name, target_doc=None):
#     from frappe.model.mapper import get_mapped_doc

#     # Map fields from Patient to Payment Entry
#     doclist = get_mapped_doc(
#         "Customer",
#         source_name,
#         {
#             "Customer": {
#                 "doctype": "Sales Invoice",
#                 "field_map": {
#                     "customer_name": "customer",    
#                 },
#             }
#         },
#         target_doc,
#     )
#     return doclist




import frappe

@frappe.whitelist()
def generate_doctor_invoice(customer_name):
    
    # print(f"\n\n{customer_name}\n\n")
    sales_invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": customer_name,
        "items": [
            {
                "item_code": "Doctor Charges",  
                "qty": 1,
                "rate": 1000,  
            }
        ]
    })
    sales_invoice.insert()
    # sales_invoice.submit()

    return frappe.utils.get_url_to_form("Sales Invoice", sales_invoice.name)



#  appointement to sales invoice

# @frappe.whitelist()
# def generate_appointment_invoice(appointment_name):
#     """
#     Generate a Sales Invoice for the services provided in an Appointment.
#     """
   
#     appointment = frappe.get_doc('Appointment', appointment_name)

   
#     sales_invoice = frappe.get_doc({
#         "doctype": "Sales Invoice",
#         "customer": appointment.customer_name,
#         "items": [
#             {
#                 "item_code": "Doctor Charges",  
#                 "qty": 1,
#                 "rate": 1000  
#             }
#         ]
#     })
#     sales_invoice.insert()

  
#     return sales_invoice.name





@frappe.whitelist()
def generate_appointment_invoice(appointment_name):
    
  
    appointment = frappe.get_doc('Appointment', appointment_name)

 
    if not appointment.customer_name:
        frappe.throw("Customer is required to create a Sales Invoice.")

    # Create the Sales Invoice
    sales_invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": appointment.customer_name,
        "posting_date": frappe.utils.today(),
        "due_date": frappe.utils.add_days(frappe.utils.today(), 2),
        "items": [
            {
                "item_code": "Doctor Charges",  # Replace with a valid item code from your system
                "qty": 1,
                "rate": 1000  # Replace with dynamic rate if needed
            }
        ]
    })

    # Insert and submit the Sales Invoice
    sales_invoice.insert(ignore_permissions=True)

    return sales_invoice.name

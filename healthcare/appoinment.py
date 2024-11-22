import frappe
def before_save(doc, event):
    if doc.is_new() and not frappe.db.exists("User", doc.customer_email):
			
        user = frappe.new_doc("User")
        user.email = doc.customer_email
        user.first_name = doc.customer_name
        user.enabled = 1
        user.append("roles", {"role": "Patient"})
        user.save(ignore_permissions=True)

        frappe.msgprint(f"User {doc.customer_email} created with the Patient role.")
   
        
        
        
    # set user permission
    
    if doc.is_new() and frappe.db.exists("User", doc.customer_email):
			
        user = frappe.new_doc("User Permission")
        user.user = doc.custom_doctor_email
        user.allow = "Customer"
        user.for_value = doc.customer_name
        user.save(ignore_permissions=True)

    
    
    
    
    

   


    # doctor_email = frappe.db.get_value("Doctor", doc.custom_doctor, "email")
    # if not doctor_email:
    #     frappe.throw(f"The selected Doctor '{doc.custom_doctor}' does not have an email address set.")
    
    # # Check if a User already exists with this email
    # if not frappe.db.exists("User", doctor_email):
    #     frappe.throw(f"No User exists with the email '{doctor_email}'. Please create a User for this Doctor.")
    
    # # Optionally, set user permissions for the Doctor's email (if needed)
    # if not frappe.db.exists("User Permission", {"user": frappe.session.user, "for_value": doctor_email}):
    #     frappe.get_doc({
    #         "doctype": "User Permission",
    #         "user": frappe.session.user,
    #         "allow": "Doctor",
    #         "for_value": doctor_email
    #     }).insert(ignore_permissions=True)
        
    frappe.msgprint("success")

